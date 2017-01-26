"""Url definitions for the rank API."""

from django.conf.urls import url

import magicranker.api.views


urlpatterns = [
    url(r'^rank/', magicranker.api.views.rank),
    url(r'^get_all_controls/', magicranker.api.views.get_all_controls),
]
