from django.core.mail import send_mail
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
        update_count = 0;

        # Add stock_list to the db if they aren't there already
        if stocks:
            for stock in stocks:
                print stock
                stock, created = Detail.objects.get_or_create(code=stock)
                if created:
                    new_count += 1;
                    stock.first_listed = today
                else:
                    update_count += 1;

                stock.last_listed = today
                stock.save()
        else:
            logging.error('Failed to download stock list')

        message = 'Stock list report ran at {0}\n'.format(
                datetime.now())
        message = '{0} new companies\n'.format(new_count)
        message += '{0} updated companies'.format(update_count)

        title = 'Report: stock list complete' 
        logging.info(message)

        send_mail(
            title, message, 'reports@magicranker.com',
            ['lextoumbourou@gmail.com'], fail_silently = False)

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

        title = 'Report: unlisted companies complete'
        message = 'Unlisted company report ran at {0}\n'.format(
                datetime.now())
        message += '{0} unlisted companies'.format(unlisted_count)

        send_mail(
             title, message, 'reports@magicranker.com',
            ['lextoumbourou@gmail.com'], fail_silently = False)

    def handle(self, *args, **kwargs):
        self._get_full_stock_list()
