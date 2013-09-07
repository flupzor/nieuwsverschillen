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

class NOSNLParser(BaseParser):
    feeder_base = 'http://www.nos.nl'
    feeder_pat  = '^http://www.nos.nl/artikel/'

    def _parse(self, html):
        soup = BeautifulSoup(html)

        self.meta = soup.findAll('meta')

        article = soup.find('div', id = 'article')
        self.title = article.find('h1').getText()

        article_content = soup.find('div', id = 'article-content')

        page_last_modified = article_content.find('abbr', 'page-last-modified')
        if page_last_modified:
            self.date = page_last_modified.getText()

        self.body = ''
        for i in article_content.children:
            if not isinstance(i, Tag):
                continue
            if not i.name == 'p':
                continue

            self.body += i.getText() + '\n\n'

