from django.contrib import admin
from nieuwsverschillen.models import Article, ArticleVariant

class ArticleVariantInline(admin.TabularInline):
    model = ArticleVariant

class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleVariantInline, ]

admin.site.register(Article, ArticleAdmin)
