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
