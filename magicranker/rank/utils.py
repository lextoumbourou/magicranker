from magicranker.rank.Ranker import RankMethod, FilterMethod


def get_rank_methods(form_data):
    output = []
    if form_data.get('rank_roe'):
        # Roe is ordered from highest to lowest
        output.append(RankMethod(
            name='roe',
            min=form_data.get('rank_roe_min', 0.05),
            max=form_data.get('rank_roe_max', 0.70),
            average=form_data.get('rank_roe_avg', 0),
            ascending=False))
    if form_data.get('rank_pe'):
        # Pe is ordered from lowest to highest
        output.append(RankMethod(
            name='pe',
            min=form_data.get('rank_pe_min', 0),
            max=form_data.get('rank_pe_max')))

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
            name='total_debt_ratio', max=form_data.get('filter_debt_max')))

    return output
