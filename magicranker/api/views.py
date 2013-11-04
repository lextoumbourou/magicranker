import json

from django.core.cache import cache
from django.http import HttpResponse

from magicranker.rank.Ranker import Ranker
from magicranker.rank import forms as rank_forms, utils as rank_utils


def rank(request):
    if request.method == 'GET':
        form = rank_forms.RankForm(request.GET)
        if form.is_valid():
            rank_methods = rank_utils.get_rank_methods(form.cleaned_data)
            filter_methods = rank_utils.get_filter_methods(form.cleaned_data)

            if 'limit' in form.cleaned_data:
                limit = int(form.cleaned_data['limit'])
            else:
                limit = None
            data = cache.get(hash(tuple(rank_methods + filter_methods)))
            data = None
            if not data:
                ranker = Ranker(
                    rank_methods, filter_methods, limit)
                data = ranker.process()

                cache.set(
                    hash(tuple(rank_methods + filter_methods)),
                    data,  60*60*24)

            rank_results = data.to_json(orient='records')
        else:
            rank_results = json.dumps([])

        return HttpResponse(rank_results, mimetype='application/json')
