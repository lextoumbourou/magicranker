import datetime as dt
from decimal import Decimal

from django.core.management.base import BaseCommand
from magicranker.stock.models import PriceHistory, Detail
from magicranker.backend.scrapers.YahooFinance import YahooFinance

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        stocks = Detail.objects.all()
        for stock in stocks:
            yf = YahooFinance(stock.code)
            results = yf.get_price_history()

            if not results: continue

            header = results.next()
            for r in results:
                if not r: continue
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
                price_data.adj_close = Decimal(adj_close)
                price_data.save()
