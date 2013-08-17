from django.db import models
from django.utils import timezone

from json_field import JSONField

from datetime import timedelta

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

    article = models.ForeignKey(Article)

    download_date = models.DateTimeField(auto_now_add=True)
    http_content = models.TextField()
    http_headers = JSONField()

    parsed_content = models.TextField()

