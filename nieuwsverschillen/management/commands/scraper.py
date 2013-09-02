from django.core.management.base import BaseCommand

from nieuwsverschillen.models import Source


class Command(BaseCommand):
    help = "Scraper"

    def handle(self, *args, **options):
        for source in Source.objects.all():
            source.update_articles()
