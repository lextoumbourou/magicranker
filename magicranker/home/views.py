"""Simple views for rendering home page."""

from django.views.generic import View
from django.shortcuts import render


class HomeView(View):

    """Render the home page."""

    def get(self, request):
        return render(request, 'home.html', {})
