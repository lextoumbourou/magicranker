import datetime as dt

import pandas as pd

from django.test import TestCase
from magicranker.stock.utils import get_price_data


class StockTest(TestCase):
    fixtures = ['price_data.yaml']

    def testReturnListOfPricesForStocks(self):
        stocks = ['ANZ', 'CBA', 'NAB']
        start = dt.datetime(year=2012, month=7, day=1)
        end = dt.datetime(year=2013, month=6, day=30)

        price_data = get_price_data(stocks, start, end)

        self.assertIsInstance(price_data, pd.core.frame.DataFrame)
