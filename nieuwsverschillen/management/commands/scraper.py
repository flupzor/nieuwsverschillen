from django.core.management.base import BaseCommand

from nieuwsverschillen.scraper import ArticleScraper


class Command(BaseCommand):
    help = "Scraper"

    def handle(self, *args, **options):
        for article_scraper in ArticleScraper.objects():
            article_scraper.scrape_article()
