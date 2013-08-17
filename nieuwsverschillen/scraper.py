import logging
logger = logging.getLogger(__name__)

from django.conf import settings

from nieuwsverschillen.models import Article, ArticleVariant
from nieuwsverschillen.management.commands.utils import load_parser, parser_by_path

import requests

class ArticleScraper(object):
    def __init__(self, article):
        self.article = article

    @classmethod
    def objects(self):

        # Update the article list
        for parser_path in settings.NIEUWSVERSCHILLEN_PARSERS :
            parser_class = load_parser(parser_path)

            # Retrieve the index page.
            response = requests.get(parser_class.feeder_base)
            # XXX: verify content-type etc...

            # Extract all the article urls from the index page.
            url_list = parser_class.feed_urls(response.text)

            for url in url_list:
                logger.debug("Creating a Article object for: {0}".format(url))
                # Look if we've tried to download it before.
                article, created = Article.objects.get_or_create(url = url,
                    parser_path=parser_path)

        # Return a list of the Articles wrapped in a ArticleScraper.
        for article in Article.objects.all():
            if article.should_be_updated():
                yield ArticleScraper(article)

    def http_client(self):
        req_headers = {}

        article = self.article

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

    def article_parser(self, article_variant):
        article = self.article

        self.parser_class = parser_by_path(article.parser_path)
        self.parser = parser_class(article.url, article_variant.http_content)

        article_variant.parsed_content = parser.body

        # Dispose of this article variant if an article variant with the same
        # content already exists.
        if article_variant.content_already_exists():
            logger.debug("SKIPPING SAME CONTENT")
            return

        logger.debug("NEW ARTICLE FOUND")

        article_variant.save()

    def scrape_article(self):
        article_variant = self.http_client()
        if article_variant:
            self.article_parser(article_variant)
