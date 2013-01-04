from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^info/?', direct_to_template, {'template': 'info.html'}),
    url(r'^contact/?', direct_to_template, {'template': 'contact.html'}),
    url(r'^rank/?', 'magicranker.rank.views.rank'),
    url(r'^$', 'magicranker.rank.views.main'),
)
