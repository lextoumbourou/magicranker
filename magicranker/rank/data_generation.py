import datetime as dt
from dateutil.relativedelta import relativedelta
from operator import itemgetter

from django.db.models import Avg

from magicranker.stock.models import PerShare, Detail, BalSheet

AVERAGE_VALUES = ['roe']
AVERAGE_YEARS = [3, 5, 10]

def get_current_pershare(stock):
    today = dt.datetime.now()
    last_year = today - relativedelta(years=1)
    results = (PerShare.objects
       .filter(code=stock.pk)
       .filter(date__lte=today)
       .filter(date__gte=last_year)
       .order_by('-date'))
    try:
        return results.values()[0]
    except IndexError:
        return False

def get_debt_percentage(stock):
    bal_sheet = BalSheet.objects.filter(code=stock).order_by('-period_ending')[0]

    if bal_sheet.total_liabilities and bal_sheet.total_assets:
        return (bal_sheet.total_liabilities / float(bal_sheet.total_assets))

    return None

def get_average(stock, value, years):
    today = dt.datetime.now()
    end = today - relativedelta(years=years)
    results = (PerShare.objects
       .filter(code=stock.pk)
       .filter(date__lte=today)
       .filter(date__gte=end)
       .order_by('-date'))
    average = results.aggregate(Avg(value))
    return average[value + '__avg']

        
def process():
    """ Return an alphabetically sorted list of dictionary including all the filterable
    and rankable values 

    Performance is not an issue here. This is designed to be run daily and placed into 
    Memcache or Redis
    """
    output = []
    for stock in Detail.objects.filter(is_listed=True):
        detail = {}
        detail['code'] = stock.code
        detail['name'] = stock.name
        current_data = get_current_pershare(stock)
        if not current_data:
            continue
        detail.update(current_data)
        detail['debt_percentage'] = get_debt_percentage(stock)

        for value in AVERAGE_VALUES:
            for years in AVERAGE_YEARS:
                detail['{0}__avg__{1}'.format(value, years)] = get_average(stock, value, years)

        output.append(detail)

    # Sort by name
    output = sorted(output, key=itemgetter('code'))

    return output

if __name__ == '__main__':
    print process()
