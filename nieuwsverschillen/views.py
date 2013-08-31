from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import get_object_or_404
from django.db.models import Count

from nieuwsverschillen.models import Article, ArticleVariant

from nieuwsverschillen.diff_match_patch import diff_match_patch

class ArticleList(ListView):
    model = Article
    paginate_by = 6

    def get_queryset(self):
        manager = self.model._default_manager
        has_variations = self.request.GET.get('has_variations')

        queryset = manager.annotate(Count('articlevariant'))

        if has_variations:
            queryset = queryset.filter(articlevariant__count__gt = 1)
        else:
            queryset = queryset

        return queryset.all()

    def get_context_data(self, **kwargs):
        from nieuwsverschillen.scraper import ArticleScraper

        context = super(ArticleList, self).get_context_data(**kwargs)

        # Copied this bit from django-paging.
        query_dict = self.request.GET.copy()
        if 'page' in query_dict:
            del query_dict['page']

        context.update({
            'querystring': query_dict.urlencode(),
        })

        return context

class ArticleDetail(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)

        variant_list = context['object'].articlevariant_set.all()

        cmp_list = []
        for i in range(len(variant_list)):
            n = i + 1
            if n < len(variant_list):
                cmp_list.append( (variant_list[i], variant_list[n]) )

        context['cmp_list'] = cmp_list

        return context

class DiffView(TemplateView):
    template_name = 'nieuwsverschillen/diffview.html'

    def diff_prettyHtml(self, diffs):
        """Convert a diff array into a pretty HTML report.

        Args:
          diffs: Array of diff tuples.

        Returns:
          HTML representation.
        """
        html = []
        for (op, data) in diffs:
            text = (data.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace("\n", "<br>"))
            if op == diff_match_patch.DIFF_INSERT:
                html.append("<ins style=\"background:#e6ffe6;\">%s</ins>" % text)
            elif op == diff_match_patch.DIFF_DELETE:
                html.append("<del style=\"background:#ffe6e6;\">%s</del>" % text)
            elif op == diff_match_patch.DIFF_EQUAL:
                html.append("<span>%s</span>" % text)

        return "".join(html)

    def get_context_data(self, **kwargs):
        context = super(DiffView, self).get_context_data(**kwargs)
        r1 = self.request.GET.get('r1')
        r2 = self.request.GET.get('r2')

        r1_obj = get_object_or_404(ArticleVariant, pk=r1)
        r2_obj = get_object_or_404(ArticleVariant, pk=r2)

        context['diff'] = self.diff_prettyHtml(r1_obj.diff_to(r2_obj))

        return context

class ArticleParse(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        from nieuwsverschillen.scraper import ArticleScraper

        context = super(ArticleParse, self).get_context_data(**kwargs)

        obj = context['object']

        scraper = ArticleScraper(obj)
        for variant in obj.articlevariant_set.all():
            scraper.article_parser(variant)

        return context
