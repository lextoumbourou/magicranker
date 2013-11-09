import os
import json

from django.core.cache import cache
from django.http import HttpResponse

from magicranker.rank.Ranker import Ranker
from magicranker.rank import forms as rank_forms, utils as rank_utils


def rank(request):
    if request.method == 'POST':
        data = json.loads(request.raw_post_data)
        rank_methods = [method for method in data['rank_methods'] if method['is_selected']]
        filter_methods = [method for method in data['filter_methods'] if method['is_selected']]

        if 'limit' in data:
            limit = int(data['limit'])
        else:
            limit = 50
        data = cache.get(hash(request.raw_post_data))
        if not data:
            ranker = Ranker(
                rank_methods, filter_methods, limit)
            data = ranker.process()

            cache.set(
                hash(request.raw_post_data),
                data,  60*60*24)

        rank_results = data.to_json(orient='records')
    else:
        rank_results = json.dumps([])

    return HttpResponse(rank_results, mimetype='application/json')


def get_all_controls(request):
    path = os.path.dirname(__file__)
    data = json.load(open(os.path.join(path, 'json/rank_controls.json')))
    return HttpResponse(json.dumps(data), mimetype='application/json')
