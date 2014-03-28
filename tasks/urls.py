#-*-encoding=utf-8-*-
from django.conf.urls import patterns, url

urlpatterns = patterns('tasks.views',
                       url(r'^$', 'index'),
                       url(r'^amazon/$', 'amazon'),
                       url(r'^duokan/$', 'duokan'),
                       url(r'^douban/$', 'douban'),
                       url(r'^ikandou/$', 'ikandou'),
                       )
