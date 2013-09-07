from baseparser import BaseParser
from bs4 import BeautifulSoup, Tag, Comment


class TelegraafParser(BaseParser):
    feeder_base = 'http://www.telegraaf.nl'
    feeder_pat  = '^http://www.telegraaf.nl/(overgeld|binnenland|buitenland)/\d+/'

    def _parse(self, html):
        soup = BeautifulSoup(html)

        self.meta = soup.findAll('meta')

        article = soup.find('div', id = 'artikel')
        title = article.find('h1')

        self.title = ''
        for i in title.children:
            # Skip comments
            if isinstance(i, Comment):
                continue

            self.title += i.lstrip()

        date = article.find('div', 'artDatePostings')
        self.date = date.find('span', 'datum').getText()

        article_column = soup.find('div', id = 'artikelKolom')

        self.body = ""
        for i in article_column.children:
            if not isinstance(i, Tag):
                continue
            if not i.name == 'p':
                continue
            self.body += i.getText() + '\n\n'
