from django.core.management.base import BaseCommand

from django.conf import settings

from nieuwsverschillen.models import ArticleVariant

import itertools

class Command(BaseCommand):
    help = "similarities"
    def handle(self, *args, **options):
        variants = ArticleVariant.objects.all()

        for v0, v1 in itertools.combinations(variants, 2):
            # Skip articles on the same site
            if v0.article.source == v1.article.source:
                continue

            if v0.is_similar(v1):
                logger.debug("Found a similar version %d, %d", v0.pk, v1.pk)

                v0.similar_versions.add(v1)
                v0.save()
