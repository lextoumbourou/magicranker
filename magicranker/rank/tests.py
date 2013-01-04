from magicwatchlists.stock.models import *
from magicwatchlists.rank.lib.ranker import *
from magicwatchlists.watch.models import *
from magicwatchlists.rank.lib.ranker import *
from django.utils import unittest
from django.db.models.query import * 
from datetime import datetime

class RankerTest(unittest.TestCase):
    def setUp(self):
        # Create some sample data
        anz = Details.objects.get_or_create(code='ANZ', name='ANZ Bank', desc='A company 1')
        PerShare.objects.create(code=anz[0], 
                                date=datetime.now(),
                                earnings='2.5',
                                roe='0.3',
                                book_value='3',
                                pe='8.3',
                                market_cap='10000000')

        nab = Details.objects.get_or_create(code='NAB', name='NAB Bank', desc='A company 2')
        PerShare.objects.create(code=nab[0], 
                                date=datetime.now(),
                                earnings='3.5',
                                roe='0.2',
                                book_value='4',
                                pe='7.3',
                                market_cap='10000200')

        cba = Details.objects.get_or_create(code='CBA', name='CBA Bank', desc='A company 3')
        PerShare.objects.create(code=cba[0], 
                                date=datetime.now(),
                                earnings='2.2',
                                roe='0.25',
                                book_value='3',
                                pe='5.3',
                                market_cap='6000200')

        wow = Details.objects.get_or_create(code='WOW', name='Woolies', desc='A company 4')
        PerShare.objects.create(code=wow[0],
                                date=datetime.now(),
                                earnings='2.4',
                                roe='0.43',
                                book_value='5',
                                pe='9.3',
                                market_cap='7543678')

        roe_rank = RankMethod(name='roe', order='-roe')
        pe_rank = RankMethod(name='pe', min=5, order='pe')
        rank_methods = [roe_rank, pe_rank]

        #market_cap_filter = FilterMethod(name='market_cap', min=5000000)
        #filter_methods = [market_cap_filter]

        self.ranker = Ranker(rank_methods, [], limit=50)

    def test_rank_by_roe_returns_highest_first(self):
        roe_rank = RankMethod(name='roe', order='-roe')
        rank_methods = [roe_rank]
        ranker = Ranker(rank_methods, [], limit=50)
        results = ranker.process()

        self.assertTrue(results[0].code.code == 'WOW')

    def test_rank_by_pe_returns_lowest_first(self):
        pe_rank = RankMethod(name='pe', min=5, order='pe')
        ranker = Ranker([pe_rank], [], limit=50)
        results = ranker.process()

        self.assertTrue(results[0].code.code == 'CBA')

class RankerToWatchlistTest(unittest.TestCase):
    def setUp(self):
        # Setup rank methods
        roe_rank = RankMethod(name='roe', order='roe')
        pe_rank = RankMethod(name='pe', min=5, order='-pe')
        rank_methods = [roe_rank, pe_rank]

        # Setup filter methods
        market_cap_filter = FilterMethod(name='market_cap', min=5000000)
        filter_methods = [market_cap_filter]
        ranker = Ranker(rank_methods, filter_methods)

        # Get or create a user
        u = User.objects.get_or_create(username='lex', 
                                       email='lextoumbourou@gmail.com',
                                       password='blahblah',)
        self.user = u[0]

        ranker.save_to_watchlist(self.user, 'Unit Test List', '20.95', '100000', 2008, 2010)

    def tearDown(self):
        # Delete the Unit Test List watch list
        l = List.objects.filter(name='Unit Test List', user=self.user)
            
        l.delete()

    def test_watch_list_saved_to_database(self):
        l = List.objects.filter(name='Unit Test List', user=self.user)
        # Should assert true if the list exists
        self.assertTrue(l)

    #def test_should_decide_on_purchase_date_based_on_history(self):
    #    """
    #    Expected output =
    #    datetime()
    #    """
    #    self.assertIsInstance(rtw._get_purchase_date(), datetime)

 
#    def test_should_return_false_if_not_loss(self):
#        from magicwatcher.rank.lib.ranker import *
#        roe_rank = RankMethod(name='roe', order='roe')
#        pe_rank = RankMethod(name='pe', min=5, order='-pe')
#        rank_methods = [roe_rank, pe_rank]
#        market_cap_filter = FilterMethod(name='market_cap', min=5000000)
#        filter_methods = [market_cap_filter]
#        ranker = Ranker(rank_methods, filter_methods, 50)
#        code = Details.objects.get(code='AAD')
#        year = 2011
#        cur_date = dt.datetime(year=year, month=07, day=01)
#        pre_date = dt.datetime(year=year-1, month=07, day=01)
#        cur_price = PriceHistory.objects.get(code=code, date=cur_date)
#        pre_price = PriceHistory.objects.get(code=code, date=pre_date)
#        ranker._is_loss(cur_price.close, pre_price.close)
#
#        self.assetIsFalse(self.ranker._is_loss(cur_price.close, pre_price.close))
#
#    def test_should_return_true_if_loss(self):
#        self.assertIsTrue(self.ranker._is_loss(cur_price=1.50, pre_price=1.60))
#
#    def test_should_return_price_object_pre_june(self):
#        from magicwatcher.rank.lib.ranker import *
#        from magicwatcher.stock.models import *
#        roe_rank = RankMethod(name='roe', order='roe')
#        pe_rank = RankMethod(name='pe', min=5, order='-pe')
#        rank_methods = [roe_rank, pe_rank]
#        market_cap_filter = FilterMethod(name='market_cap', min=5000000)
#        filter_methods = [market_cap_filter]
#        ranker = Ranker(rank_methods, filter_methods, 50)
#        stock = Details.objects.get(code='JAG')
#        year = 2011
#        ranker._get_tax_price(stock, year, True)
#            
#    def test_should_return_price_object_post_june(self):
#        from magicwatcher.rank.lib.ranker import *
#        from magicwatcher.stock.models import *
#        roe_rank = RankMethod(name='roe', order='roe')
#        pe_rank = RankMethod(name='pe', min=5, order='-pe')
#        rank_methods = [roe_rank, pe_rank]
#        market_cap_filter = FilterMethod(name='market_cap', min=5000000)
#        filter_methods = [market_cap_filter]
#        ranker = Ranker(rank_methods, filter_methods, 50)
#        stock = Details.objects.get(code='JAG')
#        year = 2011
#        ranker._get_tax_price(stock, year, False)
#        
#    def test_should_return_price_object(self):
#        from magicwatcher.rank.lib.ranker import *
#        from magicwatcher.stock.models import *
#        roe_rank = RankMethod(name='roe', order='roe')
#        pe_rank = RankMethod(name='pe', min=5, order='-pe')
#        rank_methods = [roe_rank, pe_rank]
#        market_cap_filter = FilterMethod(name='market_cap', min=5000000)
#        filter_methods = [market_cap_filter]
#        ranker = Ranker(rank_methods, filter_methods, 50)
#        stock = Details.objects.get(code='JAG')
#        date = dt.datetime(year=2011, month=6, day=25)
#        ranker._get_price(stock, date)
#        
#def test_should_retun_true_if_loss(self):
#    cur_price = PriceHistory.objects.get(date)
