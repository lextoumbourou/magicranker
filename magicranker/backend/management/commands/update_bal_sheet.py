from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

from magicranker.backend.scrapers import YahooFinance
from magicranker.stock.models import BalSheet


class Command(BaseCommand):
    help = 'Get Balance Sheet Details from YahooFinance'

    def handle(self, *args, **kwargs):
        stocks = Detail.objects.filter(is_listed=True)
        for stock in stocks:
            yf = YahooFinance.YahooFinance(stock.code)
            data = yf.get_bal_sheet()
            print data
            return False



