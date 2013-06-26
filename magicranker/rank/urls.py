from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    'magicranker.main.views',
    url(r'^/rank', 'rank'),
    url(r'^$', 'main'),
)
