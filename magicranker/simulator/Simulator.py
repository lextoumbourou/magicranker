import pandas as pd
from decimal import Decimal

from magicranker.stock.models import PriceHistory


class Simulator(object):
    def __init__(self, size, price_data=None):
        """ Take a list of stocks to buy, a start and end date and a portfolio size

        args:
            size - float representing portfolio size
            price_data - panda Timeseries object with a stock id as the column,
                         then it will be collected from the database

        To do: 
            * allow to specify a buy algorithm (though I don't know much about this yet)
              (by default just purchase them all on the first day)
        """
        self.size = size
        self.price_data = price_data

        self.total = None

    def build_price_data(self, stocks, start_date, end_date, record='close'):
        """ Return a pandas TimeSeries object with price data for a list of stocks

        return:
            pandas.core.frame.DataFrame
        """
        if not self.price_data:
            data = PriceHistory.objects.filter(
                code__code__in=stocks,
                date__gte=start_date,
                date__lte=end_date)

            self.price_data = data.to_timeseries(
                index='date', pivot_columns='code',
                values=record, storage='long')

    def generate_purchase_amounts(self):
        """ Return a dictionary that represents number of stocks to purchase for each stock
        based on a portion of the portfolio size to allocate and the first price for the stock
        """
        columns = self.price_data.columns
        first_row = self.price_data.head(1)
        buys = {}
        parcel_price = float(self.size) / len(columns)
        for column in columns:
            buys[column] = Decimal(parcel_price) / first_row[column][0]

        return buys


    def run(self):
        """ Go through each timestamp object and multiple the stock price by the buy size and generate a total
        Save to total attribute
        """
        if not self.price_data:
            raise NoPriceData

        total = self.price_data.copy()
        buys = self.generate_purchase_amounts()
        # Multiple each stock by the number of stocks bought
        for buy in buys:
            total[buy] = total[buy] * buys[buy]

        self.total = total.sum(1)
