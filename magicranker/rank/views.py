from django.core.cache import cache
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext

from forms import RankForm
from magicranker.rank.Ranker import RankMethod, FilterMethod, Ranker


def main(request):
    return render_to_response('rank.html', {})


def rank(request):
    """
    Handle calls to the ranker module and cache
    """
    args = {}
    if request.method == 'GET' and request.GET:
        form = RankForm(request.GET)
        if form.is_valid():
            print "Cleaned data: "
            print form.cleaned_data
            rank_methods = get_rank_methods(form.cleaned_data)
            filter_methods = get_filter_methods(form.cleaned_data)
            if 'limit' in form.cleaned_data:
                limit = int(form.cleaned_data['limit'])
            else:
                limit = None
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

def get_rank_methods(form_data):
    output = [] 
    if form_data.get('rank_roe'):
        # Roe is ordered from highest to lowest
        output.append(RankMethod(
            name='roe', 
            min=form_data.get('rank_roe_min', 0.05),
            max=form_data.get('rank_roe_max', 0.70), 
            average=form_data.get('rank_roe_avg', 0), 
            desc=True))
    if form_data.get('rank_pe'):
        # Pe is ordered from lowest to highest
        output.append(RankMethod(
            name='pe', 
            min=form_data.get('rank_pe_min', 0),
            max=form_data.get('rank_pe_max')))
    if form_data.get('rank_martet_cap'):
        # Market Cap is ordered from highest to lowest
        output.append(RankMethod(
            name='market_cap', 
            min=form_data.get('rank_market_cap_min'),
            order='market_cap'))
    if form_data.get('rank_debt'):
        # Debt is ordered from lowest to highest
        output.append(RankMethod(
            name='debt_per', 
            max=form_data.get('rank_debt_max'),
            order='-debt_per'))

    return output

def get_filter_methods(form_data):
    output = []
    if 'filter_roe' in form_data:
        # Roe is ordered from highest to lowest
        output.append(FilterMethod(
            name='roe', min=form_data.get('roe_rank_min'),
            max=form_data.get('roe_rank_max')))
    if 'filter_pe' in form_data:
        # Pe is ordered from lowest to highest
        output.append(FilterMethod(
            name='pe', min=form_data.get('pe_rank_min'),
            max=form_data.get('pe_rank_max')))
    if 'filter_market_cap' in form_data:
        # Market Cap is ordered from highest to lowest
        output.append(FilterMethod(
            name='market_cap', min=form_data.get('filter_market_cap_min')))
    if 'filter_debt' in form_data:
        # Debt is ordered from lowest to highest
        output.append(FilterMethod(
            name='debt_per', max=form_data.get('filter_debt_max')))

    return output
