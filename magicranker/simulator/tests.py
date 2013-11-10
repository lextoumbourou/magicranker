import pandas as pd
import datetime as dt
from django.test import TestCase

import utils


class SimulateTest(TestCase):
    def testCanGetTimestamps(self):
        price_data = pd.DataFrame([
            {'date': dt.datetime(2011, 1, 1)},
            {'date': dt.datetime(2011, 2, 1)},
            {'date': dt.datetime(2011, 1, 1)},
        ])
        timestamps = utils.get_timestamps(price_data)
        self.assertEquals(len(timestamps), 2)

    def testCanGenerateBuysEvenly(self):
        price_data = pd.DataFrame([
            {'code': 'CBA', 'date': dt.datetime(2011, 1, 1), 'close': 10},
            {'code': 'ANZ', 'date': dt.datetime(2011, 1, 1), 'close': 25},
        ], index=['CBA', 'ANZ'])
        portfolio_size = 1000
        symbols = ['CBA', 'ANZ']
        data = utils.generate_buys_evenly(price_data, portfolio_size, symbols)
        self.assertEquals(data['CBA'], 50)
        self.assertEquals(data['ANZ'], 20)

    def testSimulateReturnsADataSet(self):
        start_date = dt.datetime(2011, 1, 1)
        end_date = dt.datetime(2011, 1, 2)
        price_data = pd.DataFrame([
            {'code': 'CBA', 'date': start_date, 'close': 10.15},
            {'code': 'ANZ', 'date': start_date, 'close': 25},
            {'code': 'CBA', 'date': end_date, 'close': 11},
            {'code': 'ANZ', 'date': end_date, 'close': 26},
        ], index=['CBA', 'ANZ', 'CBA', 'ANZ'])
        portfolio_size = 1000
        symbols = ['CBA', 'ANZ']
        buys = {
            'CBA': 50,
            'ANZ': 20
        }
        results = utils.simulate(price_data, buys, start_date, end_date)
        self.assertEquals(results['CBA'][0], 10.15 * 50)
