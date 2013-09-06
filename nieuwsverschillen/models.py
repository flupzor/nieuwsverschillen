from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify

from nieuwsverschillen.diff_match_patch import diff_match_patch
from nieuwsverschillen.management.commands.utils import load_parser, parser_by_path

from json_field import JSONField
from datetime import timedelta
from urlparse import urlparse

import requests

import logging
logger = logging.getLogger(__name__)

class Source(models.Model):
    url = models.CharField(max_length=255, blank=False, unique=True)
    slug = models.SlugField(blank=False)
    description = models.TextField(blank=True, null=True)

    # Which parser should be used for this site.
    parser_path = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        # automatically fill the slug.
        url_slug = urlparse(self.url).netloc.replace('.', '-')
        self.slug = slugify(url_slug)

        super(Source, self).save(*args, **kwargs)

    @property
    def parser_class(self):
        return parser_by_path(self.parser_path)

    def update_articles(self):
        parser_class = self.parser_class

        # Retrieve the index page.
        response = requests.get(parser_class.feeder_base)
        # XXX: verify content-type etc...

        # Extract all the article urls from the index page.
        url_list = parser_class.feed_urls(response.text)

        for url in url_list:
            logger.debug("Creating a Article object for: {0}".format(url))
            # Look if we've tried to download it before.
            article, created = Article.objects.get_or_create(url = url,
                source=self)

        # Update all articles which have this source.
        for article in self.article_set.all():
            article.fetch()

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse

        # XXX: for now redirect to article-list.
        return reverse('article-list', args=[self.slug])

class Article(models.Model):
    source = models.ForeignKey(Source)

    slug = models.SlugField(blank=False)

    url = models.CharField(max_length=255, blank=False, unique=True)

    # statistics
    nr_requests = models.IntegerField(default=0)
    nr_downloads = models.IntegerField(default=0)
    last_download_date = models.DateTimeField(auto_now_add=True)

    seen_in_overview = models.DateTimeField(auto_now_add=True)

    # http
    http_last_modified = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # automatically fill the slug.

        # XXX: the slug is based on a variant of this article. The title,
        # can vary between variants. So this mightn't be the best
        # solution.
        self.slug = slugify(self.article_title)

        super(Article, self).save(*args, **kwargs)

    def http_client(self):
        req_headers = {}

        article = self

        if article.http_last_modified:
            req_headers.update({
                'If-Modified-Since': article.http_last_modified
            })

        debug_msg = "GET \"{0}\" last modified: \"{1}\"".format(article.url,
            article.http_last_modified)
        logger.debug(debug_msg)

        response = requests.get(article.url, headers=req_headers)

        if response.status_code == requests.codes.not_modified:
            # update statistics
            article.nr_requests += 1
            article.save()

            logger.debug("Not modified")

            return None

        # update the statistics
        article.nr_requests += 1
        article.nr_downloads += 1
        article.save()

        http_headers = {}

        if 'last-modified' in response.headers:
            article.http_last_modified = response.headers['last-modified']
            article.save()
            logger.debug("Last modified: \"{0}\"".format(article.http_last_modified))
        elif 'date' in response.headers:
            article.http_last_modified = response.headers['date']
            article.save()
            logger.debug("Last modified: \"{0}\"".format(article.http_last_modified))

        article_variant = ArticleVariant(article = article, http_content =
            response.text, http_headers = dict(response.headers))

        return article_variant


    def fetch(self):
        if self.should_be_updated():
            article_variant = self.http_client()
            if article_variant:
                article_variant.parse()

    @property
    def article_title(self):
        return self.articlevariant_set.all()[0].article_title

    @property
    def article_content(self):
        return self.articlevariant_set.all()[0].article_content

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('article-detail', args=[self.source.slug,
            self.slug])

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

        # XXX: there should be an lower limit too. E.g. every 5 minutes.

        return True

class ArticleVariant(models.Model):
    """ Model with the raw article data. This data can be used to
    regenerate the other database models when the parsing code gets
    updated """

    article = models.ForeignKey(Article)

    # HTTP data which shouldn't be modified after they're created.
    http_download_date = models.DateTimeField(auto_now_add=True)
    http_content = models.TextField()
    http_headers = JSONField()

    # The article which is parsed from the HTTP data.
    article_title = models.TextField()
    article_content = models.TextField()

    def content_already_exists(self):
        for variant in self.article.articlevariant_set.all():
            if variant != self and self.compare(variant):
                return True

        return False

    def compare(self, variant):
        """ Compare this variant to another. Return True if they are equal.
        False otherwise. """

        if self.article_title != variant.article_title:
            return False

        if self.article_content != variant.article_content:
            return False

        return True

    def diff(self, variant):
        """ Create a diff between this variant and another """

        dmp = diff_match_patch()
        diff = dmp.diff_main(self.article_content, variant.article_content)
        dmp.diff_cleanupSemantic(diff)

        return diff

    def parse(self):
        article = self.article

        parser_class = parser_by_path(article.source.parser_path)
        parser = parser_class(article.url, self.http_content)

        self.article_content = parser.body
        self.article_title = parser.title

        # Dispose of this article variant if an article variant with the
        # same content already exists.
        if self.content_already_exists():
            if self.pk:
                self.delete()
            logger.debug("SKIPPING SAME CONTENT")
            return

        logger.debug("NEW ARTICLE FOUND")

        self.save()

