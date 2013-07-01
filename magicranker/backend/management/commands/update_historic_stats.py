import time
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail

from magicranker.backend.scrapers.ETrade import ETrade
from magicranker.stock.models import Detail, PerShare
import magicranker._private as private

class Command(BaseCommand):
    def add_to_db(self, stock, data):
        for count in range(0, len(data['periods'])):
            kwargs = {}
            kwargs['code'] = stock
            kwargs['date'] = data['periods'][count]
            try:
                kwargs['shares_outstanding'] = float(data['shares_out'][count]) * 1000000
            except IndexError:
                kwargs['shares_outstanding'] = None
            try:
                kwargs['earnings'] = data['earnings'][count]
            except IndexError:
                kwargs['earnings'] = None
            try:
                kwargs['roe'] = data['roe'][count]
            except IndexError:
                kwargs['roe'] = None
            try:
                kwargs['book_value'] = data['book_value'][count]
            except IndexError:
                kwargs['book_value'] = None
            try:
                kwargs['pe'] = data['pe'][count]
            except IndexError:
                kwargs['pe'] = None

            # check if the record exists
            try:
                obj = PerShare.objects.get(code=stock, date=kwargs['date'])
                print 'Already exists for ', stock
                print 'Updating'
                obj.roe = kwargs['roe']
                obj.shares_outstanding = kwargs['shares_outstanding']
                obj.book_value = kwargs['book_value']
                obj.earnings = kwargs['earnings']
                obj.pe = kwargs['pe']
                obj.save()
            except PerShare.DoesNotExist:
                print 'Adding record for ', stock
                print kwargs
                obj = PerShare(**kwargs)
                obj.save()

    def handle(self, *args, **kwargs):
        stocks = Detail.objects.all()
        etrade = ETrade()
        etrade.login(
            username=private.ETRADE_USERNAME, password=private.ETRADE_PASSWORD)
        scrape_count = 0
        error_count = 0
        for stock in stocks:
            time.sleep(1)
            print stock.code
            data = etrade.get_data(stock)
            print data
            if data:
                try:
                    self.add_to_db(stock, data)
                    scrape_count += 1
                except Exception as e:
                    print "Can't add to database: " + str(e)
                    error_count += 1
        title = 'Report: update historical stats ({0})'.format(
                datetime.now())
        message = '{0} companies updated\n'.format(scrape_count)
        message += '{0} companies failed to update\n'.format(error_count)
        send_mail(
            title, message, 'reports@magicranker.com',
            ['lextoumbourou@gmail.com'], fail_silently = False)

