import datetime as dt

from django.core.management.base import BaseCommand
from magicranker.stock.models import PriceHistory

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        stocks = Detail.objects.all()
        for stock in stocks:
            yf = YahooFinance.YahooFinance(stock.code)
            results = yf.get_price_history()

            if not results: continue

            for r in results[1:]:
                date_str, open_price, high, low, \
                close, volume, adj_close = r
                date = dt.datetime.strptime(date_str, '%Y-%m-%d')
                price_data, created = PriceHistory.objects.get_or_create(
                    code=stock, date=date)
                price_data.open = open_price
                price_data.high = high
                price_data.low = low
                price_data.close = close
                price_data.volume = volume
                price_data.adj_close = adj_close
                price_data.save()
