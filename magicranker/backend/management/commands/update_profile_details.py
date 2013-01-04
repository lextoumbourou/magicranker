from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, CommandError

from magicranker.backend.scrapers import YahooFinance
from magicranker.stock.models import Detail


class Command(BaseCommand):
    help = 'Get Profile Details from YahooFinance'

    def handle(self, *args, **kwargs):
        stocks = Detail.objects.filter(is_listed=True)
        for stock in stocks:
            yf = YahooFinance.YahooFinance(stock.code)
            code, name, description = yf.get_profile()
            stock.name = name
            stock.desc = description
            stock.save()
