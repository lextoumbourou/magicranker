from django.conf.urls import patterns, url, include
from magicranker.api import views


urlpatterns = patterns('',
    url(r'^rank/', 'magicranker.api.views.rank'),
    url(r'^simulate_rank/', 'magicranker.api.views.simulate_rank'),
    url(r'^get_all_controls/', 'magicranker.api.views.get_all_controls'),
)
