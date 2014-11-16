"""Simple views for rendering home page."""

from django.views.generic import View
from django.shortcuts import render_to_response
from django.template import RequestContext


class HomeView(View):

    """Render the home page."""

    def get(self, request):
        return render_to_response(
            'home.html', {}, context_instance=RequestContext(request))
