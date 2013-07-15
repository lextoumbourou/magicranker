from operator import itemgetter
import datetime as dt
from dateutil.relativedelta import relativedelta

from django.db.models import Avg

from magicranker.stock.models import PerShare, Detail


class RankMethod():
    def __init__(self, name, average=False,
                 min=False, max=False, desc=False):
        self.name = name
        self.average = average
        self.min = min
        self.max = max
        self.desc = desc
		

class FilterMethod():
    def __init__(self, name, average=False,
                 min=False, max=False, filter_after=False):
        self.name = name
        self.min = min
        self.max = max


class Ranker():
    def __init__(self, rank_methods, filter_methods, limit=50):
        # List of RankMethod() objects
        self.rank_methods = rank_methods
        # List of FilterMethod() objects
        self.filter_methods = filter_methods
        self.limit = limit

    def _get_filtered_query(self, rank_method, date=None):
        """ Return a list of PerShare objects converted to dicts
        one per company in the market

        If average is requested in the rank_method, also get the averaged value for the 
        time period requested
        """
        stocks = []
        average = None

        if not date:
            date = dt.datetime.now()

        for stock in Detail.objects.filter(is_listed=True):
            current = {}
            if rank_method.average:
                old_date = date - relativedelta(years=rank_method.average)
            else:
                old_date = date - relativedelta(years=1)

            results = (PerShare.objects
               .filter(code=stock.pk)
               .filter(date__lte=date)
               .filter(date__gte=old_date)
               .order_by('-date'))

            average = {}
            # Get average
            if rank_method.average:
                average = results.aggregate(Avg(rank_method.name))

            try:
                current = results.values()[0]
            except IndexError:
                continue

            # If we don't have data for the company that goes back far enough
            # we skip them
            if results[results.count()-1].date.year == old_date.year:
                continue

            current.update(average)
            current['name'] = stock.name
            current['code'] = stock.code
            
            filter_key = rank_method.name
            if rank_method.average:
                filter_key = filter_key + '__avg'

            if not current[filter_key]:
                continue

            stocks.append(current)

        return stocks

    def _get_rank(self, rank_method, stocks):
        """ Sort list of dictionary either by name requested
        in rank_method of by the averaged value
        """
        output = []

        sort_key = rank_method.name
        if rank_method.average:
            sort_key = sort_key + '__avg'

        stocks = sorted(
            stocks, key=itemgetter(sort_key),
            reverse=rank_method.desc)

        # Sort the list of dictionaries by the rank method
        for rank, stock in enumerate(stocks):
            # Create a dictionary mapping of stock object to rank
            result = {stock['code_id']: (rank + 1, stock)}
            output.append(result)

        return output

    def _get_total_rank(self, rank_results):
        """ Get the ranked data and add it together to get the total rank
        """
        output = {}
        for name, ranks in rank_results.iteritems():
            for rank in ranks:
                for stock_id, data in rank.iteritems():
                    rank_value = data[0]
                    stock_obj = data[1]
                    # Don't append stock if it doesn't
                    # match filter criteria
                    will_append = True

                    for method in self.filter_methods + self.rank_methods:
                        filter_key = method.name
                        if hasattr(method, 'average') and method.average:
                            avg_filter_key = filter_key + '__avg'
                            if avg_filter_key in stock_obj:
                                filter_key = avg_filter_key

                        if ((method.min and (stock_obj[filter_key] < method.min)) or
                           (method.max and (stock_obj[filter_key] > method.max)) or 
                           (stock_obj[filter_key] is None)):
                            will_append = False
                            break

                    # Increment value or initialise
                    if will_append:
                        if stock_id in output:
                            current_rank = output[stock_id]['rank']
                            output[stock_id]['rank'] = current_rank + rank_value
                        else:
                            output[stock_id] = stock_obj
                            output[stock_id]['rank'] = rank_value

        # Convert a list of dicts and sort
        unsorted_stocks = [d for _, d in output.iteritems()]
        return sorted(unsorted_stocks, key=itemgetter('rank'))[:self.limit]

    def _is_loss(self, cur_price, pre_price):
        """ Take two decimal objects (current & previous) and determines 
        whether you've made a loss or not

        ** Not currently implemented **
        """
        if cur_price < pre_price:
            return True
        else:
            return False

    def _get_price(self, stock, date, order=''):
        """ Return the closest possible price based on a date

        ** Not currently implemented **
        """
        # Make a 5 day range to select from
        if not order:
            start = date
            end = date + dt.timedelta(days=5)
        else:
            start = date - dt.timedelta(days=5)
            end = date

        price_obj = PriceHistory.objects.filter(code=stock)

        # Select the earliest in that range 
        price_obj = price_obj.filter(date__range=(start, end))
        # Can't buy stocks on a weekend
        price_obj = price_obj.exclude(date__week_day=6).exclude(date__week_day=7)
        price_obj = price_obj.order_by(order+'date')[0]
                    
        return price_obj

    def _get_tax_price(self, stock, year, is_loss=False):
        """ Return a price object before or after the tax
        year depending on whether you've made a win or a loss

        ** Not currently implemented **
        """
        if not is_loss:
            date = dt.datetime(year=year, month=07, day=01)
            price = self._get_price(stock, date)
        else:
            date = dt.datetime(year=year, month=06, day=30)
            price = self._get_price(stock, date, order='-')

        return price

    def process(self):
        ranks = {}
        for rank_method in self.rank_methods:
            stocks = self._get_filtered_query(rank_method)
            ranks[rank_method.name] = self._get_rank(rank_method, stocks)

        final = self._get_total_rank(ranks)
        return final
