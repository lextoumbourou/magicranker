import datetime as dt
from django.db.models import Max

from magicranker.stock.models import PerShare

from operator import itemgetter


class RankMethod():
    def __init__(self, name, average=False,
                 min=False, max=False, order=False):
        self.name = name
        self.averge = average
        self.min = min
        self.max = max
        self.order = order
		

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

    def _get_filtered_query(self, date=None):
        """
        Returns a PerShare queryset, based on filter parameters
        """
        if not date:
            date = dt.datetime.now()

        last_year = date - dt.timedelta(days=365)
        # Get filtered items as close as possible 
        # to date in between the year, used for performing
        # a rank in the past
        results = (PerShare.objects
           .filter(date__lte=date)
           .filter(date__gte=last_year)
           .order_by('code', '-date')
           .distinct('code__code'))

        for method in self.filter_methods + self.rank_methods:
            if method.min:
                filter = method.name + '__gte'
                results = results.filter(**{filter: method.min})
            if method.max:
                filter = method.name + '__lte'
                results = results.filter(**{filter: method.max})

        # Built in filters to clear out negative returns
        results = results.filter(roe__gt=0).filter(pe__gt=0)

        return results.values_list('pk', flat=True)

    def _get_rank(self, queryset):
        """
        Returns a dict with ranked values
        """
        output = {}
        query = PerShare.objects.filter(pk__in=queryset)

        for method in self.rank_methods:
            output[method.name] = []
            count = 1
            for val in query.order_by(method.order):
                # Create a dictionary mapping of stock object to rank
                if val:
                    result = {val:count}
                    output[method.name].append(result)
                    count += 1

        return output

    def _get_total_rank(self, rank_results):
        """
        Adds the rank, to get the total rank
        """
        output = {}
        for name, ranks in rank_results.iteritems():
            for rank in ranks:
                for stock, count in rank.iteritems():
                    # Increment value or initialise
                    output[stock] = output.get(stock, 0) + count
        return output

    def _sort(self, dict_to_sort, limit):
        """
        Sorts the dictionary mapping to tupple
        """
        output = []
        first_sort = sorted(dict_to_sort.items(), key=itemgetter(1))[:limit]
        for f in first_sort:
            output.append(f[0])

        return output

    def _is_loss(self, cur_price, pre_price):
        '''
        Takes two decimal objects (current & previous) and determines 
        whether you've made a loss or not
        '''
        if cur_price < pre_price:
            return True
        else:
            return False

    def _get_price(self, stock, date, order=''):
        '''
        Return the closest possible price based on a date
        '''
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
        '''
        Returns a price object before or after the tax
        year depending on whether you've made a win or a loss
        '''
        if not is_loss:
            date = dt.datetime(year=year, month=07, day=01)
            price = self._get_price(stock, date)
        else:
            date = dt.datetime(year=year, month=06, day=30)
            price = self._get_price(stock, date, order='-')

        return price

    def process(self):
        query = self._get_filtered_query()
        ranks = self._get_rank(query)
        final_rank = self._get_total_rank(ranks)
        return self._sort(final_rank, self.limit)
