from datetime import datetime
from magicranker.stock.models import PerShare, Detail
from dateutil.relativedelta import relativedelta


class RankMethod():
    def __init__(self, name, average=False,
                 min=False, max=False, ascending=True):
        self.name = name
        self.average = average
        self.min = min
        self.max = max
        self.ascending = ascending
		

class FilterMethod():
    def __init__(self, name, min=False, max=False):
        self.name = name
        self.min = min
        self.max = max
        self.average = False


class Ranker():
    def __init__(self, rank_methods, filter_methods, limit=50):
        # List of RankMethod() objects
        self.rank_methods = rank_methods
        # List of FilterMethod() objects
        self.filter_methods = filter_methods
        self.limit = limit

    def process(self):
        today = datetime.today()

        results = PerShare.objects

        # Build up the filter using the requested filters
        # also, determine how much data to pull from the db
        # based on the highest average value requested
        highest = 1
        for method in self.rank_methods + self.filter_methods:
            if method.average and method.average > highest:
                highest = method.average
                # If they have requested the values to be averaged, 
                # we'll do the filtering after pulling from the db
                continue
            if method.min:
                filter = method.name + '__gte'
                results = results.filter(**{filter: method.min})
            if method.max:
                filter = method.name + '__lte'
                results = results.filter(**{filter: method.max})
            

        period_starts = today - relativedelta(years=highest)
        results = results.filter(date__lte=today).filter(date__gt=period_starts)
        results = results.order_by('code__code', 'year', '-date').distinct('code__code', 'year')

        # Create a list of fields in model to use as arguments (there might be a better way to do this)
        fields = [f.name for f in PerShare._meta.fields[1:]]

        # Convert data to a Pandas dataframe for easy processing. This is the slowest step in the process
        data = results.to_dataframe(
            'code__name', 'code__code', *fields, index='code', coerce_float=True)

        ## Just get this years data
        this_years_data = data[data.year == today.year]

        # Create an empty rank table filled with zeros
        this_years_data['total_rank'] = 0

        # Create the ranks and do the filtering on averaged values
        for method in self.rank_methods:
            # Average if requested
            if method.average and method.average > 1:
                this_years_data[method.name] = (
                    data[method.name].astype(float).groupby(data.index).mean())
                # Filter on the averages
                if method.min:
                    this_years_data = this_years_data[this_years_data[method.name] > method.min]
                if method.max:
                    this_years_data = this_years_data[this_years_data[method.name] < method.max]

            this_years_data['total_rank'] += (
                this_years_data[method.name].rank(ascending=method.ascending))

        return this_years_data.sort(['total_rank', 'code__code'])[:self.limit]
