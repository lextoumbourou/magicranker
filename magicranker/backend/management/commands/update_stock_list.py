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

        new_count = 0;
        updated_count = 0;

        # Add stock_list to the db if they aren't there already
        if stocks:
            for stock in stocks:
                stock, created = Detail.objects.get_or_create(
                    code=stock, name='', desc='',
                    last_listed=today)
                if created:
                    new_count += 1;
                    stock.first_listed = today
                else:
                    update_count += 1;
                    stock.last_listed = today

                stock.save()
                self.stdout.write('Adding or updating {0}\n'.format(stock))
            return True
        else:
            logging.error('Failed to download stock list')
            return False

    def handle(self, *args, **kwargs):
        if self._get_full_stock_list():
            self._set_unlisted_companies()
