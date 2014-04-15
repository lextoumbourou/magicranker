# -*- coding: utf-8 -*-
import os
import json

from flask import Blueprint, render_template, jsonify

mod = Blueprint('api', __name__)

@mod.route('/api/v1/rank')
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

    return rank_results

@mod.route('/api/v1/get_controls')
def get_controls():
    path = os.path.dirname(__file__)
    data = json.load(open(os.path.join(path, 'json/rank_controls.json')))
    return jsonify(data)
