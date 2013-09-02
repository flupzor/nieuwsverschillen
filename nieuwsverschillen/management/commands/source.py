from django.core.management.base import BaseCommand

from django.conf import settings
from nieuwsverschillen.management.commands.utils import load_parser, parser_by_path

from nieuwsverschillen.models import Source

class Command(BaseCommand):
    help = "Source"
    def handle(self, *args, **options):
        for path in settings.NIEUWSVERSCHILLEN_PARSERS:
            parser_class = load_parser(path)

            source, created = Source.objects.get_or_create(url = parser_class.feeder_base,
                parser_path = path)
            source.save()
