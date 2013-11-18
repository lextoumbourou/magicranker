import pandas as pd
import datetime as dt
from django.test import TestCase

import utils

from Simulator import Simulator


class SimulateTest(TestCase):
    #def test_get_price_data_returns_a_timeseries(self):
    #    stocks = ['ANZ', 'CBA', 'NAB']
    #    start_date = dt.datetime(2011, 1, 1)
    #    end_date = dt.datetime(2011, 3, 1)
    #    size = 1000000

    #    sim = Simulator(size)
    #    sim.build_price_data(stocks, start_date, end_date)
    #    self.assertIsInstance(sim.price_data, pd.core.frame.DataFrame)

    def test_simulator_run(self):
        size = 100
        price_data = pd.DataFrame(
            [{1: 1.20, 2: 2.30},
             {1: 1.30, 2: 2.40}], 
            index=pd.Series(
                [dt.datetime(2011, 1, 1), dt.datetime(2011, 1, 2)])
        )
        sim = Simulator(size, price_data)
        sim.run()
        self.assertTrue(type(sim.total) == pd.core.series.TimeSeries)
        purchase_1 = 50 / 1.20
        purchase_2 = 50 / 2.30
        first_total = (1.20 * purchase_1) + (2.30 * purchase_2)
        second_total = (1.30 * purchase_1) + (2.40 * purchase_2)
        self.assertTrue(sim.total[0] == first_total)
        self.assertTrue(sim.total[1] == second_total)
