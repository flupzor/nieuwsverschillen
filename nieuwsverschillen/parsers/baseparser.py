import re

import logging
logger = logging.getLogger(__name__)

from bs4 import BeautifulSoup

# Base Parser
# To create a new parser, subclass and define _parse(html).
class BaseParser(object):
    url = None
    domains = [] # List of domains this should parse

    # These should be filled in by self._parse(html)
    date = None
    title = None
    byline = None
    body = None

    real_article = True # If set to False, ignore this article
    SUFFIX = ''         # append suffix, like '?fullpage=yes', to urls

    meta = []  # Currently unused.

    # Used when finding articles to parse
    feeder_base = None  # Look for links on this page
    feeder_pat = None   # matching this regular expression

    feeder_bs = BeautifulSoup #use this version of beautifulsoup for feed

    def __init__(self, url, html):
        self.url = url
        self.html = html
        self._parse(self.html)

    def _parse(self, html):
        """Should take html and populate self.(date, title, byline, body)

        If the article isn't valid, set self.real_article to False and return.
        """
        raise NotImplementedError()

    @classmethod
    def feed_urls(cls, html):
        soup = cls.feeder_bs(html)

        # "or ''" to make None into str
        urls = [a.get('href') or '' for a in soup.findAll('a')]

        # If no http://, prepend domain name
        domain = '/'.join(cls.feeder_base.split('/')[:3])
        urls = [url if '://' in url else domain + url for url in urls]

        return [url for url in urls if re.search(cls.feeder_pat, url)]
