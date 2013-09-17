from django.test import TestCase
from django.db.models.query import * 
from datetime import datetime

from magicranker.stock.models import PerShare, Detail
from magicranker.rank.Ranker import *


class RankerTest(TestCase):
    fixtures = ['rank_stock_data.yaml']

    def testRankByPEReturnsLowestFirst(self):
        pe_rank = RankMethod(name='pe', min=5)
        ranker = Ranker([pe_rank], [], limit=50)
        results = ranker.process()

        self.assertTrue(results.code__code[0:1].values[0] == 'ARB')

    def testRankByROEReturnHighestFirst(self):
        roe_rank = RankMethod(name='roe', max=0.70, ascending=False)
        ranker = Ranker([roe_rank], [], limit=50)
        results = ranker.process()

        self.assertTrue(results.code__code[0:1].values[0] == 'SRX')

    def testRankAndFilterRemovesTooSmallCompanies(self):
        market_cap_filter = FilterMethod(name='market_cap', min=5000000)
        roe_rank = RankMethod(name='roe', max=0.70, ascending=False)

        ranker = Ranker([roe_rank], [market_cap_filter], limit=50)
        results = ranker.process()

        self.assertTrue(results.code__code[0:1].values[0] == 'CBA')

    def testRankROEAndPEReturnsCorrectTop(self):
        roe_rank = RankMethod(name='roe', max=0.70, ascending=False)
        pe_rank = RankMethod(name='pe', min=5)

        ranker = Ranker([pe_rank, roe_rank], [], limit=50)
        results = ranker.process()

        self.assertTrue(results.code__code[0:1].values[0] == 'SRX')

    def testRankROEAvg5ReturnsCorrectTop(self):
        roe_rank = RankMethod(name='roe', max=0.80, average=5, ascending=False)

        ranker = Ranker([roe_rank], [], limit=50)
        results = ranker.process()

        self.assertTrue(results.code__code[0:1].values[0] == 'ARB')
        self.assertTrue(results.code__code[-1:].values[0] == 'ANZ')

    # This feature hasn't been written yet
    #def testRankAndFilterRemovesCompaniesWithHighDebt(self):
    #    debt_filter = FilterMethod(name='debt_percentage', max=0.50)
    #    roe_rank = RankMethod(name='roe', max=10, ascending=False)
    #    ranker = Ranker([roe_rank], [debt_filter], limit=50)
    #    results = ranker.process()

    #    import pdb; pdb.set_trace()
    #    self.assertTrue(all([result['code'] != 'SRX' for result in results]))
    #    self.assertTrue(any([result['code'] == 'ANZ' for result in results]))
    #    self.assertTrue(len(results) == 2)
