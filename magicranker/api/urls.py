from django.conf.urls import patterns, url, include
from magicranker.api import views


urlpatterns = patterns('',
    url(r'^rank/', 'magicranker.api.views.rank'),
)
