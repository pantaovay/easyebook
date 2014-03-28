from django.conf.urls import patterns, url

urlpatterns = patterns('spider.views',
        url(r'^$', 'index'),
        url(r'^amazon/(?P<category>\w+)/$', 'amazon'),
        url(r'^duokan/$', 'duokan'),
        url(r'^douban/$', 'douban'),
        url(r'^ikandou/$', 'ikandou'),
        url(r'^total/$', 'total')
)