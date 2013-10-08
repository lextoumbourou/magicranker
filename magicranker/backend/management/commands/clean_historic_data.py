from django.core.management.base import BaseCommand, CommandError
from magicranker.stocks.models import PerShare

class Command(BaseCommand):
    def _update_years(self):
        stocks = PerShare.objects.all()
        for stock in stocks:
            if stock.date:
                stock.year = stock.date.year
                stock.save()

    def handle(self, *args, **kwargs):
        self._update_years()


