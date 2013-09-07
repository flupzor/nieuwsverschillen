# Copyright (c) 2013 Alexander Schrijver <alex@flupzor.nl>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from baseparser import BaseParser
from bs4 import BeautifulSoup, Tag


class NuNLParser(BaseParser):
    feeder_base = 'http://www.nu.nl/'
    feeder_pat  = '^http://www.nu.nl/\w+/\d+/'

    def _parse(self, html):
        soup = BeautifulSoup(html)

        header = soup.find('div', 'header')

        self.meta = soup.findAll('meta')
        self.title = header.find('h1').getText()

        # Date of the last revision
        self.date = header.find('div', 'dateplace-data').contents[2].lstrip()

        content = soup.find('div', 'content')

        self.body = ''
        self.body += soup.find('h2', 'summary').getText() + '\n\n'

        article_body = content.find('div', 'main-articlebody')

        for i in article_body.children:
            if not isinstance(i, Tag):
                continue
            if not i.name == 'h2' and not i.name == 'p':
                continue

            self.body += i.getText() + '\n\n'

