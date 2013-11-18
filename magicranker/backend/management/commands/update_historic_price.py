import datetime as dt
from decimal import Decimal
import time

from django.core.management.base import BaseCommand
from magicranker.stock.models import PriceHistory, Detail
from magicranker.backend.scrapers.YahooFinance import YahooFinance


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        stocks = Detail.objects.all()
        for stock in stocks:
            if PriceHistory.objects.filter(code=stock).count() > 100:
                print "skipping ", stock.code
                continue

            print "Working on ", stock.code
            yf = YahooFinance(stock.code)
            results = yf.get_price_history()

            if not results: continue

            header = results.next()
            for r in results:
                if not r: continue
                print r
                date_str, open_price, high, low, \
                close, volume, adj_close = r
                date = dt.datetime.strptime(date_str, '%Y-%m-%d')
                price_data, created = PriceHistory.objects.get_or_create(
                    code=stock, date=date)
                price_data.open = Decimal(open_price)
                price_data.high = Decimal(high)
                price_data.low = Decimal(low)
                price_data.close = Decimal(close)
                price_data.volume = Decimal(volume)
                price_data.adjusted_close = Decimal(adj_close)
                try:
                    price_data.save()
                except:
                    print "Failed to save ", stock.code, " data: ", r
            time.sleep(0.2)
