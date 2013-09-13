# Copyright (c) 2012 Eric Price, Jennifer 8. Lee, Greg Price, and contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

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

        return set([url for url in urls if re.search(cls.feeder_pat, url)])
