from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Parser"
    def handle(self, *args, **options):
        self.stdout.write("Parser")

