from django.core.management.base import BaseCommand, CommandError

from magicranker.backend.scrapers import ETrade
from magicranker.stock.models import Detail, PerShare

class Command(BaseCommand):
    def add_to_db(self, stock, data):
        for count in range(0, len(data['periods'])):
            print count
            kwargs = {}
            kwargs['code'] = stock
            kwargs['period'] = data['periods'][count]
            kwargs['shares_out'] = data['shares_out'][count]
            kwargs['earnings'] = data['earnings'][count]
            kwargs['roe'] = data['roe'][count]
            kwargs['book_value'] = data['book_value'][count]

            # check if the record exists
            try:
                obj = PerShare.objects.get(code=stock, period=kwargs['period'])
                print 'Already exists for ', stock
                print 'Updating'
                obj.roe = kwargs['roe']
                obj.shares_out = kwargs['shares_out']
                obj.book_value = kwargs['book_value']
                obj.earnings = kwargs['earnings']
                obj.save()
            except PerShare.DoesNotExist:
                print 'Adding record for ', stock
                print kwargs
                obj = PerShare(**kwargs)
                obj.save()

    def handle(self, *args, **kwargs):
        stocks = Details.objects.all()
        etrade = ETrade()
        etrade.login(username=private.username, password=private.password)
        scrape_count = 0
        for stock in stocks:
            time.sleep(1)
            print stock.code
            data = etrade.get_data(stock)
            if data:
                try:
                    self.add_to_db(stock, data)
                except:
                    print "Can't add to database"
        title = 'Report: update historical stats ({0})'.format(
                datetime.now())
        message = '{0} companies updated'.format(scrape_count)
        send_mail(
            title, message, 'reports@magicranker.com',
            ['lextoumbourou@gmail.com'], fail_silently = False)

