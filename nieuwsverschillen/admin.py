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

from django.contrib import admin
from django.db.models import Count
from nieuwsverschillen.models import Article, ArticleVersion

class ArticleVersionInline(admin.TabularInline):
    model = ArticleVersion

class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleVersionInline, ]

    list_display = ["url", "similar_articles__count"]

    def queryset(self, request):
        qs = super(ArticleVersionAdmin, self).queryset(request)
        return qs.annotate(Count('similar_articles'))

    def similar_articles__count(self, obj):
        return obj.similar_articles__count

class ArticleVersionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleVersion, ArticleVersionAdmin)
