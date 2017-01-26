from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView

from .home.views import HomeView
import magicranker.api.urls

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^info/?', TemplateView.as_view(template_name='info.html')),
    url(r'^contact/?', TemplateView.as_view(template_name='contact.html')),
    url(r'^api/?', include(magicranker.api.urls)),
    url(r'^favicon\.ico$',
        RedirectView.as_view(url='/static/images/favicon.ico')),
    url(r'^$', HomeView.as_view()),
]
