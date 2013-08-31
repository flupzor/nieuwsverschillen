from django.core.management.base import BaseCommand

from nieuwsverschillen.models import ArticleVariant
from nieuwsverschillen.scraper import ArticleScraper

class Command(BaseCommand):
    help = "Parser"
    def handle(self, *args, **options):
        # re-parse all the articles.

        for variant in ArticleVariant.objects.all():
            scraper = ArticleScraper(variant.article)

            scraper.article_parser(variant)

