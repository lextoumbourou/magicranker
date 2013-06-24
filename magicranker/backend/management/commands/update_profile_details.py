from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, CommandError

from magicranker.backend.scrapers import YahooFinance
from magicranker.stock.models import Detail


class Command(BaseCommand):
    help = 'Get Profile Details from YahooFinance'

    def handle(self, *args, **kwargs):
        stocks = Detail.objects.filter(is_listed=True)
        update_count = 0
        for stock in stocks:
            self.stdout.write('Updating {0}\n'.format(stock.code))
            yf = YahooFinance.YahooFinance(stock.code)
            code, name, description = yf.get_profile()

            code = code.encode('ascii', 'ignore')
            name = name.encode('ascii', 'ignore')
            description = description.encode('ascii', 'ignore')

            self.stdout.write(
                'Got the following details: {0}\n {1}\n {2}\n'.format(
                    code, name, description))

            stock.name = name
            stock.desc = description
            stock.save()
            update_count += 1

        title = 'Report: update profile details complete ({0})'.format(
                datetime.now())

        message = '{0} companies updated'.format(update_count)

        send_mail(
            title, message, 'reports@magicranker.com',
            ['lextoumbourou@gmail.com'], fail_silently = False)
