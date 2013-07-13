from django.test import TestCase
from django.db.models.query import * 
from datetime import datetime

from magicranker.stock.models import PerShare, Detail
from magicranker.rank.Ranker import *


class RankerTest(TestCase):
    fixtures = ['rank_stock_data.yaml']

    def testRankByPEReturnsLowestFirst(self):
        pe_rank = RankMethod(name='pe', min=5, desc=False)
        ranker = Ranker([pe_rank], [], limit=50)
        results = ranker.process()

        self.assertTrue(results[0]['code'] == 'ARB')

    def testRankByROEReturnHighestFirst(self):
        roe_rank = RankMethod(name='roe', max=0.70, desc=True)
        ranker = Ranker([roe_rank], [], limit=50)
        results = ranker.process()

        self.assertTrue(results[0]['code'] == 'SRX')

    def testRankAndFilterRemovesTooSmallCompanies(self):
        market_cap_filter = FilterMethod(name='market_cap', min=5000000)
        roe_rank = RankMethod(name='roe', max=0.70, desc=True)

        ranker = Ranker([roe_rank], [market_cap_filter], limit=50)
        results = ranker.process()

        self.assertTrue(results[0]['code'] == 'CBA')

    def testRankROEAndPEReturnsCorrectTop(self):
        roe_rank = RankMethod(name='roe', max=0.70, desc=True)
        pe_rank = RankMethod(name='pe', min=5, desc=False)

        ranker = Ranker([pe_rank, roe_rank], [], limit=50)
        results = ranker.process()

        self.assertTrue(results[0]['code'] == 'SRX')
        self.assertTrue(results[-1]['code'] == 'ANZ')

    def testRankROEAvg5ReturnsCorrectTop(self):
        roe_rank = RankMethod(name='roe', max=0.80, average=5, desc=True)

        ranker = Ranker([roe_rank], [], limit=50)
        results = ranker.process()

        self.assertTrue(results[0]['code'] == 'ARB')
        self.assertTrue(results[-1]['code'] == 'ANZ')
