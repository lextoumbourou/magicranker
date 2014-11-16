from django.core.management.base import BaseCommand

from magicranker.backend.scrapers import YahooFinance
from magicranker.stock.models import BalSheet, Detail


class Command(BaseCommand):
    help = 'Get Balance Sheet Details from YahooFinance'

    def handle(self, *args, **kwargs):
        stocks = Detail.objects.filter(is_listed=True)
        for stock in stocks:
            print stock.code
            yf = YahooFinance.YahooFinance(stock)
            data = yf.get_bal_sheet()
            if not data:
                continue

            if 'period_ending' in data:
                dates = data['period_ending']

            for count, date in enumerate(dates):
                if not date:
                    continue

                print "Stock is ", stock
                print "Date is ", date

                for key in data:
                    if key == 'period_ending':
                        continue

                    obj, created = BalSheet.objects.get_or_create(
                        code=stock, period_ending=date)

                    result = data[key][count]
                    setattr(obj, key, result)
                    obj.save()
