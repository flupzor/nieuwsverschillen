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

from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import get_object_or_404
from django.db.models import Count

from nieuwsverschillen.models import Article, ArticleVersion, Source

from nieuwsverschillen.diff_match_patch import diff_match_patch

class ArticleList(ListView):
    model = Article
    paginate_by = 6

    def get_queryset(self):
        manager = self.model._default_manager
        has_variations = self.request.GET.get('has_variations')
        has_similar_items = self.request.GET.get('has_similar_items')

        queryset = manager.annotate(Count('articleversion'))
        queryset = queryset.annotate(Count('similar_articles'))

        # Filter by source, if supplied
        source_slug = self.kwargs.get('source_slug', None)
        if source_slug == "all":
            pass
        elif source_slug:
            source = Source.objects.get(slug=source_slug)
            queryset = queryset.filter(source=source)

        # Only show articles with variations.
        if has_variations:
            queryset = queryset.filter(articleversion__count__gt = 1)

        # Only show articles with similar items.
        if has_similar_items:
            queryset = queryset.filter(similar_articles__count__gt = 1)

        return queryset.all()

    def get_context_data(self, **kwargs):
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

        version_list = context['object'].articleversion_set.order_by('http_download_date').all()

        cmp_list = []
        for i in range(len(version_list)):
            n = i + 1
            if n < len(version_list):
                cmp_list.append( (version_list[i], version_list[n]) )

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

        r1_obj = get_object_or_404(ArticleVersion, pk=r1)
        r2_obj = get_object_or_404(ArticleVersion, pk=r2)

        context['r1'] = r1_obj
        context['r2'] = r2_obj
        context['diff'] = self.diff_prettyHtml(r1_obj.diff(r2_obj))

        return context

# XXX: a debug view.
class ArticleParse(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleParse, self).get_context_data(**kwargs)

        obj = context['object']

        for version in obj.articleversion_set.all():
            version.parse()

        return context
