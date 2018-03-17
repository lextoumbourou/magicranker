from datetime import datetime
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

import concurrent.futures

from magicranker.backend.scrapers import yahoo_finance
from magicranker.stock.models import Detail, PriceHistory, PerShare, BalSheet

logging.config.dictConfig(settings.LOGGING)

logger = logging.getLogger(__name__)


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
        logger.info('{0}: Fetching price data'.format(stock.code))

        price_data = yahoo_finance.get_current_price(stock.code)

        if not price_data:
            logging.warning('{0}: No price data found'.format(stock))
            return False

        logger.info('{0}: Got price data: {1}'.format(stock.code, price_data))

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

        logger.info('{0}: Saved price data'.format(stock.code))

        return True

    def _update_key_stats(self, stock, date):
        """Get key statistics (relies on date collected above)."""
        try:
            stats_data = yahoo_finance.get_key_stats(stock.code)
        except yahoo_finance.StockNotFound:
            logger.info('{0}: Stock not found'.format(stock.code))
            return

        logger.info('{0}: Got stats data: {1}'.format(stock.code, stats_data))

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
        per_share.shares_outstanding = stats_data.shares_outstanding
        per_share.save()

        logger.info('{0}: Stats updated succesfully.'.format(stock.code))

        return True

    def _do_stock(self, stock):
        date = datetime.today().date()

        if self._update_latest_price(stock, date):
            self._update_key_stats(stock, date)
            self.scrape_count += 1

    def handle(self, *args, **kwargs):
        self.scrape_count = 0

        stocks = Detail.objects.filter(is_listed=True)

        # Based on example here:
        # https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            future_to_stock = {
                executor.submit(self._do_stock, stock): stock
                for stock in stocks}

            for future in concurrent.futures.as_completed(future_to_stock):
                stock = future_to_stock[future]
                try:
                    future.result()
                except Exception as exc:
                    logger.error(
                        '{0}: Exception occured: {1}'.format(stock.code, exc))
                else:
                    logger.info('{0}: Successfully updated'.format(stock.code))
