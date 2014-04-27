from dateutil.relativedata import relativedata

from .models import PerShare


def process_methods(data):
    rank_methods = [
        method for method in data['rank_methods'] if method['is_selected']]
    filter_methods = [
        method for method in data['filter_methods'] if method['is_selected']]
    limit = int(data['limit'])

    return rank_methods, filter_methods, limit
