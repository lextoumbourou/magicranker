from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

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
            print data
