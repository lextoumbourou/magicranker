from collections import defaultdict
from datetime import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd

from . import db
from .models import PerShare


def get_filtered_data(rank_methods, filter_methods):
    """Return filtered data from database as a Pandas dataframe

    The main goal of this function is to *only* get the data the user
    will need to minimize the size of the dataframe
    """
    highest = 1
    sub = PerShare.query
    today = datetime.today().date()

    for method in rank_methods + filter_methods:
        if 'average' in method and method['average'] > highest:
            highest = method['average']
            # If they have requested the values to be averaged,
            # we'll do the filtering after pulling from the db
            continue
        if 'min' in method:
            column = getattr(PerShare, method['name'])
            sub = sub.filter(column > method['min'])
        if 'max' in method:
            column = getattr(PerShare, method['name'])
            sub = sub.filter(column < method['max'])

    period_starts = today - relativedelta(years=highest)
    sub = (
        sub.filter(PerShare.date < today).filter(PerShare.date > period_starts)
    )
    sub = sub.add_columns(
        db.func.rank().over(
            partition_by=[PerShare.stock_id, db.extract('year', PerShare.date)],
            order_by=PerShare.date.desc()
        ).label('ranking')
    ).subquery('sub')

    results = (
        PerShare.query.select_entity_from(sub).filter(sub.c.ranking == 1)
    )
    return results


def query_to_dataframe(data):
    """Return a pandas DataFrame from a SQLAlchemy BaseQuery object"""
    fields = PerShare.__table__.columns._data.keys()
    output = defaultdict(list)

    for item in data.all():
        output['code'].append(item.stock.code)
        output['name'].append(item.stock.name)
        for field in fields:
            output[field].append(getattr(item, field))

    df = pd.DataFrame(
        output, columns=fields + ['code', 'name'],
        index=pd.to_datetime(output['date']))
    return df


def get_cached_filtered_data(rank_methods, filter_methods):
    """Wrapper around get_filtered_data that checks cache first"""
    data = get_filtered_data(rank_methods, filter_methods)
    return query_to_dataframe(data)


def process_methods(data):
    rank_methods = []
    filter_methods = []

    for method in data['rank_methods']:
        if 'changeable' in method and method['changeable']:
            rank_methods.append(filter_method_dict(method))

    for method in data['filter_methods']:
        if 'changeable' in method and method['changeable']:
            filter_methods.append(filter_method_dict(method))

    limit = int(data['limit'])

    return rank_methods, filter_methods, limit

def filter_method_dict(method):
    output = {}
    if 'max' in method:
        output['max'] = method['max']['value']
    if 'min' in method:
        output['min'] = method['min']['value']
    if 'average' in method:
        output['average'] = method['average']['value']

    return output
