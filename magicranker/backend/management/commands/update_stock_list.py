from datetime import datetime, timedelta
import logging

from django.core.management.base import BaseCommand, CommandError

from magicranker.backend.scrapers import asx
from magicranker.stock.models import Detail


class Command(BaseCommand):
    help = 'Scrape ASX.com.au and get updated list of stocks'

    def _get_full_stock_list(self):
        """
        Get the full stock list using the asx module
        and add it to the database
        """
        # Get the list of stocks from the ASX as a list
        stocks = asx.get_full_stock_list()
        # Get today's date
        today = datetime.today()
        # Add stock_list to the db if they aren't there already
        if stocks:
            for stock in stocks:
                stock, created = Detail.objects.get_or_create(
                    code=stock, name='', desc='',
                    last_updated=today, is_listed=True)
                if not created:
                    stock.last_updated = today
                    stock.is_listed = True
                    stock.save()
                self.stdout.write('Adding or updating {0}\n'.format(stock))
            return True
        else:
            logging.error('Failed to download stock list')
            return False

    def _set_unlisted_companies(self):
        """
        Set companies that haven't been updated in 1 month, to unlisted
        """
        two_weeks_ago = (datetime.today() - timedelta(weeks=2)).date()
        stocks = Detail.objects.filter(is_listed=True)
        for stock in stocks:
            if stock.last_updated <= two_weeks_ago:
                self.stdout.write(
                    '{0} has been marked unlisted\n'.format(stock))
                stock.is_listed = False
                stock.save()

    def handle(self, *args, **kwargs):
        if self._get_full_stock_list():
            self._set_unlisted_companies()
