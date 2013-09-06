import cookielib
import re
import socket
import sys
import time
import unicodedata

import logging
logger = logging.getLogger(__name__)

from bs4 import BeautifulSoup

def strip_whitespace(text):
    lines = text.split('\n')
    return '\n'.join(x.strip().rstrip(u'\xa0') for x in lines).strip() + '\n'

# from http://stackoverflow.com/questions/5842115/converting-a-string-which-contains-both-utf-8-encoded-bytestrings-and-codepoints
# Translate a unicode string containing utf8
def parse_double_utf8(txt):
    def parse(m):
        try:
            return m.group(0).encode('latin1').decode('utf8')
        except UnicodeDecodeError:
            return m.group(0)
    return re.sub(ur'[\xc2-\xf4][\x80-\xbf]+', parse, txt)

def canonicalize(text):
    return strip_whitespace(parse_double_utf8(text))

# End utility functions

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

    def __unicode__(self):
        return canonicalize(u'\n'.join((self.date, self.title, self.byline,
                                        self.body,)))

    @classmethod
    def feed_urls(cls, html):
        soup = cls.feeder_bs(html)

        # "or ''" to make None into str
        urls = [a.get('href') or '' for a in soup.findAll('a')]

        # If no http://, prepend domain name
        domain = '/'.join(cls.feeder_base.split('/')[:3])
        urls = [url if '://' in url else domain + url for url in urls]

        return [url for url in urls if re.search(cls.feeder_pat, url)]
