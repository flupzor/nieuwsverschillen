from django.db import models
from django.utils import timezone

from json_field import JSONField

from datetime import timedelta

from nieuwsverschillen.diff_match_patch import diff_match_patch

import logging
logger = logging.getLogger(__name__)

class Article(models.Model):
    url = models.CharField(max_length=255, blank=False, unique=True)

    # Which parser should be used for this article.
    parser_path = models.CharField(max_length=255)

    # statistics
    nr_requests = models.IntegerField(default=0)
    nr_downloads = models.IntegerField(default=0)
    last_download_date = models.DateTimeField(auto_now_add=True)

    seen_in_overview = models.DateTimeField(auto_now_add=True)

    # http
    http_last_modified = models.TextField(blank=True, null=True)

    @property
    def article_title(self):
        return self.articlevariant_set.all()[0].article_title

    @property
    def article_content(self):
        return self.articlevariant_set.all()[0].article_content

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('article-detail', args=[str(self.id)])

    def __unicode__(self):
        return self.url

    def first_seen(self):
        pass

    def last_seen(self):
        pass

    def should_be_updated(self):
        # If we haven't seen the article in an overview for 2 days, don't
        # bother updating.
        if timezone.now() > self.seen_in_overview + timedelta(days=2):
            return False

        return True

class ArticleVariant(models.Model):
    """ Model with the raw article data. This data can be used to
    regenerate the other database models when the parsing code gets
    updated """

    def content_already_exists(self):
        for variant in self.article.articlevariant_set.all():
            if variant != self and self.content_equals(variant):
                return True

        return False

    def content_equals(self, variant):
        return self.parsed_content == variant.parsed_content

    def diff_to(self, variant):
        dmp = diff_match_patch()
        diff = dmp.diff_main(self.parsed_content, variant.parsed_content)
        dmp.diff_cleanupSemantic(diff)

        return diff

    article = models.ForeignKey(Article)

    # HTTP data which shouldn't be modified after they're created.
    http_download_date = models.DateTimeField(auto_now_add=True)
    http_content = models.TextField()
    http_headers = JSONField()

    # The article which is parsed from the HTTP data.
    article_title = models.TextField()
    article_content = models.TextField()

