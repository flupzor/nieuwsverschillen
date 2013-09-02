from django.core.management.base import BaseCommand

from nieuwsverschillen.models import ArticleVariant

class Command(BaseCommand):
    help = "Parser"
    def handle(self, *args, **options):
        # re-parse all articles.

        for article_variant in ArticleVariant.objects.all():
            article_variant.parse()

