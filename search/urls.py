from django.conf.urls import patterns, url

urlpatterns = patterns('search.views',
        url(r'^query/$', 'query'),
        url(r'^$', 'search')
)
