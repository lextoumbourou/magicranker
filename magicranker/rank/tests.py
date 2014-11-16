from django.test import TestCase

from magicranker.rank.Ranker import Ranker


class RankerTest(TestCase):
    fixtures = ['rank_stock_data.yaml']

    def testRankByPEReturnsLowestFirst(self):
        pe_rank = {
            'name': 'pe',
            'min': {
                'changeable': True,
                'value': 5
            },
            'ascending': True
        }
        ranker = Ranker([pe_rank], [], limit=50)
        results = ranker.process()

        self.assertTrue(results.code__code[0:1].values[0] == 'ARB')

    def testRankByROEReturnHighestFirst(self):
        roe_rank = {
            'name': 'roe',
            'max': {
                'changeable': True,
                'value': 0.70
            },
            'ascending': False
        }
        ranker = Ranker([roe_rank], [], limit=50)
        results = ranker.process()

        self.assertTrue(results.code__code[0:1].values[0] == 'SRX')

    def testRankAndFilterRemovesTooSmallCompanies(self):
        market_cap_filter = {
            'name': 'market_cap',
            'min': {
                'changeable': True,
                'value': 5000000
            },
        }
        roe_rank = {
            'name': 'roe',
            'max': {
                'changeable': True,
                'value': 0.70
            },
            'ascending': False
        }
        ranker = Ranker([roe_rank], [market_cap_filter], limit=50)
        results = ranker.process()

        self.assertTrue(results.code__code[0:1].values[0] == 'CBA')

    def testRankROEAndPEReturnsCorrectTop(self):
        roe_rank = {
            'name': 'roe',
            'max': {
                'changeable': True,
                'value': 0.70
            },
            'ascending': False
        }
        pe_rank = {
            'name': 'pe',
            'min': {
                'changeable': True,
                'value': 5
            },
            'ascending': True
        }

        ranker = Ranker([pe_rank, roe_rank], [], limit=50)
        results = ranker.process()

        self.assertTrue(results.code__code[0:1].values[0] == 'SRX')

    def testRankROEAvg5ReturnsCorrectTop(self):
        roe_rank = {
            'name': 'roe',
            'max': {
                'changeable': True,
                'value': 0.80,
            },
            'average': {
                'changeable': True,
                'value': 5
            },
            'ascending': False
        }

        ranker = Ranker([roe_rank], [], limit=50)
        results = ranker.process()

        self.assertTrue(results.code__code[0:1].values[0] == 'ARB')
        self.assertTrue(results.code__code[-1:].values[0] == 'ANZ')
