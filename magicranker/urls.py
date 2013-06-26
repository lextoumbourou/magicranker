from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^info/?', TemplateView.as_view(template_name='info.html')),
    url(r'^contact/?', TemplateView.as_view(template_name='contact.html')),
    url(r'^rank/?', 'magicranker.rank.views.rank'),
    url(r'^$', 'magicranker.rank.views.main'),
)
