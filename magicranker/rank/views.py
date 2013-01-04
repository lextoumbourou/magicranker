from django.core.cache import cache
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext

from forms import RankForm
from lib.ranker import RankMethod, FilterMethod, Ranker


def main(request):
    return render_to_response('base.html', {})


def rank(request):
    """
    Handle calls to the ranker module and cache
    """
    args = {}
    if request.method == 'GET' and request.GET:
        form = RankForm(request.GET)
        if form.is_valid():
            rank_methods = form.get_rank_methods()
            filter_methods = form.get_filter_methods()
            limit = int(form.cleaned_data['limit'])
            #data = cache.get(hash(tuple(rank_methods + filter_methods)))
            data = None
            if not data:
                ranker = Ranker(
                    rank_methods, filter_methods, limit)
                data = ranker.process()
                cache.set(
                    hash(tuple(rank_methods + filter_methods)), data,  60*60*24)

            args['rank_results'] = data
	else:
            form = RankForm()

        args['form'] = form

    return render_to_response('stock_table.html', 
                               args,
                               context_instance=RequestContext(request))
