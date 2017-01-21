from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

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

        new_count = 0
        update_count = 0

        for stock in stocks:
            stock, created = Detail.objects.update_or_create(
                code=stock.code, defaults=dict(
                    name=stock.name, category=stock.category, is_listed=True))
            if created:
                new_count += 1
                stock.first_listed = today
            else:
                update_count += 1

            stock.is_listed = True
            stock.last_listed = today
            stock.save()

            self.stdout.write('Updated {0}.\n'.format(stock))

        return new_count, update_count

    def _set_unlisted_companies(self):
        """
        Set companies that haven't been updated in 2 weeks to unlisted
        """
        two_weeks_ago = (datetime.today() - timedelta(weeks=2)).date()
        stocks = Detail.objects.filter(is_listed=True)
        unlisted_count = 0
        for stock in stocks:
            if stock.last_listed <= two_weeks_ago:
                stock.is_listed = False
                unlisted_count += 1
                stock.save()

        return unlisted_count

    def handle(self, *args, **kwargs):
        results = self._get_full_stock_list()

        if results:
            new_count, update_count = results
            unlisted_count = self._set_unlisted_companies()

            message = '{0} new companies\n'.format(new_count)
            message += '{0} updated companies\n'.format(update_count)
            message += '{0} unlisted companies'.format(unlisted_count)
        else:
            message = 'Failed to run\n'
