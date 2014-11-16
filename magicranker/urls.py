from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView

from .home.views import HomeView

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^info/?', TemplateView.as_view(template_name='info.html')),
    url(r'^contact/?', TemplateView.as_view(template_name='contact.html')),
    url(r'^rank/?', 'magicranker.rank.views.rank'),
    url(r'^api/?', include('magicranker.api.urls')),
    url(r'^favicon\.ico$',
        RedirectView.as_view(url='/static/images/favicon.ico')),
    url(r'^$', HomeView.as_view()),
)
