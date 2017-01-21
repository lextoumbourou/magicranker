import pprint

from datetime import datetime

from django.core.management.base import BaseCommand

from magicranker.backend.scrapers import yahoo_finance
from magicranker.stock.models import Detail, PriceHistory, PerShare, BalSheet


def get_total_debt_ratio(stock, date):
    data = BalSheet.objects.filter(code=stock) \
                           .filter(period_ending__lte=date) \
                           .order_by('period_ending')

    if data:
        result = data[0]
        if None not in (result.total_assets, result.total_liabilities):
            return result.total_liabilities / float(result.total_assets)


class Command(BaseCommand):

    help = 'Get Profile Details from YahooFinance'

    def _update_latest_price(self, stock, date):
        """Get latest price and update DB."""
        price_data = yahoo_finance.get_current_price(stock)

        if price_data:
            self.stdout.write(
                'Attempting to update {0}.\n'.format(
                    pprint.pprint(price_data)))
            try:
                price_history = (
                    PriceHistory.objects.get(code=stock, date=date))
            except PriceHistory.DoesNotExist:
                price_history = None

            if price_history:
                price_history.close = price_data.close
                price_history.volume = price_data.volume
            else:
                price_history = PriceHistory(
                    code=stock, date=date, close=price_data.close,
                    volume=price_data.volume)
            price_history.save()

            return True
        else:
            return False

    def _update_key_stats(self, stock, date):
        """Get key statistics (relies on date collected above)."""
        stats_data = yahoo_finance.get_key_stats(stock)

        if stats_data:
            try:
                per_share = PerShare.objects.get(
                    code=stock, date=date, year=date.year)
            except PerShare.DoesNotExist:
                per_share = None

            if not per_share:
                per_share = PerShare(
                    code=stock, date=date)

            per_share.earnings = stats_data.eps
            per_share.roe = stats_data.roe
            per_share.roa = stats_data.roa
            per_share.book_value = stats_data.bvps
            per_share.pe = stats_data.pe
            per_share.market_cap = stats_data.market_cap
            per_share.year = date.year
            per_share.total_debt_ratio = get_total_debt_ratio(stock, date)
            per_share.save()

            self.stdout.write('Update: {0}\n'.format(stats_data))

    def handle(self, *args, **kwargs):
        stocks = Detail.objects.filter(is_listed=True)
        scrape_count = 0
        for stock in stocks:
            self.stdout.write(
                'Collecting data for {0}'.format(stock))
            date = datetime.today().date()
            if self._update_latest_price(stock, date):
                self._update_key_stats(stock, date)
                scrape_count += 1
