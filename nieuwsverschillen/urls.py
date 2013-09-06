from django.conf.urls import patterns, include, url

from nieuwsverschillen.views import ArticleList, ArticleDetail, ArticleParse, DiffView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^diff/$', DiffView.as_view(), name='article-diff'),
    url(r'^s/(?P<source_slug>[\w-]+)/$', ArticleList.as_view(),
        name='article-list'),
    url(r'^s/(?P<source_slug>[\w-]+)/(?P<slug>[\w-]+)/$',
        ArticleDetail.as_view(), name='article-detail'),

    # XXX: debug view.
    url(r'^article-parse/(?P<pk>[0-9]+)/$', ArticleParse.as_view(),
        name='article-parse'),
)
