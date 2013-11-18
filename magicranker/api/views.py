import os
import json
import datetime as dt

from django.core.cache import cache
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from magicranker.rank.Ranker import Ranker
from magicranker.simulator.Simulator import Simulator
from magicranker.stock import utils as stock_utils
from magicranker.rank import forms as rank_forms, utils as rank_utils


def rank(request):
    if request.method == 'POST':
        data = get_rank_results(request)
        if data:
            rank_results = data.to_json(orient='records')
        else:
            rank_results = json.dumps([])

    return HttpResponse(rank_results, mimetype='application/json')

@csrf_exempt
def simulate_rank(request):
    if request.method == 'POST':
        data = get_rank_results(request)
        end = dt.datetime.today().date()
        start = end - dt.timedelta(days=365)

        sim = Simulator(1000000)
        sim.build_price_data(list(data.code__code.values), start, end)
        sim.run()

        return HttpResponse(sim.total.to_json(
            orient='split', double_precision=3), mimetype='application/json')


def get_all_controls(request):
    path = os.path.dirname(__file__)
    data = json.load(open(os.path.join(path, 'json/rank_controls.json')))
    return HttpResponse(json.dumps(data), mimetype='application/json')

def get_rank_results(request):
    data = json.loads(request.body)
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

    return data
