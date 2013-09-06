from baseparser import BaseParser
from bs4 import BeautifulSoup, Tag

class NOSNLParser(BaseParser):
    domains = ['www.nos.nl']

    feeder_base = 'http://www.nos.nl'
    feeder_pat  = '^http://www.nos.nl/artikel/'

    def _parse(self, html):
        soup = BeautifulSoup(html)

        self.meta = soup.findAll('meta')

        article = soup.find('div', id = 'article')
        self.title = article.find('h1').getText()

        article_content = soup.find('div', id = 'article-content')

        self.byline = ''

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

