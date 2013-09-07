import re

import logging
logger = logging.getLogger(__name__)

from bs4 import BeautifulSoup

# Base Parser
# To create a new parser, subclass and define _parse(html).
class BaseParser(object):
    url = None

    # These should be filled in by self._parse(html)
    date = None
    title = None
    body = None

    # Used when finding articles to parse
    feeder_base = None  # Look for links on this page
    feeder_pat = None   # matching this regular expression

    def __init__(self, url, html):
        self.url = url
        self.html = html
        self._parse(self.html)

    def _parse(self, html):
        """Should take html and populate self.(date, title, body)
        """
        raise NotImplementedError()

    @classmethod
    def feed_urls(cls, html):
        soup = BeautifulSoup(html)

        # "or ''" to make None into str
        urls = [a.get('href') or '' for a in soup.findAll('a')]

        # If no http://, prepend domain name
        domain = '/'.join(cls.feeder_base.split('/')[:3])
        urls = [url if '://' in url else domain + url for url in urls]

        return [url for url in urls if re.search(cls.feeder_pat, url)]
