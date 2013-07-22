from datetime import datetime
from operator import itemgetter

import data_generation


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

    def _get_rank(self, rank_method, stocks):
        """ Sort list of dictionary either by name requested
        in rank_method of by the averaged value
        """
        output = []

        sort_key = rank_method.name
        if rank_method.average:
            sort_key = '{0}__avg__{1}'.format(
                sort_key, rank_method.average)

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
                            avg_filter_key = '{0}__avg__{1}'.format(
                                filter_key, method.average)
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

    def process(self):
        ranks = {}
        today = datetime.today()
        stocks = data_generation.process()

        for rank_method in self.rank_methods:
            ranks[rank_method.name] = self._get_rank(rank_method, stocks)

        final = self._get_total_rank(ranks)
        return final
