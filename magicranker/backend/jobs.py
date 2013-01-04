from datetime import datetime, timedelta
import logging

from scrapers import YahooFinance, asx

from stock.models import Detail


def get_updated_stock_list():
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
            stock, created = StockDetails.get_or_create(
                code=stock, name='', desc='',
                last_updated=today, is_listed=True)
            if not created:
                stock.last_updated = today
                stock.is_listed = True
                stock.save()
        return True
    else:
        return False


def set_unlisted_companies():
    """
    Set companies that haven't been updated in 1 month, to unlisted
    """
    two_weeks_ago = datetime.today() - timedelta(weeks=2)
    stocks = Detail.objects.filter(is_listed=True)
    for stock in stocks:
        if stock.last_updated <= two_weeks_ago:
            stock.is_listed = False
            stock.save()


def update_profile_details(stock, yf):
    code, name, description = yf.get_profile()
    stock.name = name
    stock.desc = description
    stock.save()


def update_latest_price(stock, yf):
    # get today's price information
    price_data = yf.get_current_price()
    if price_data:
        code, date, price, volume = price_data
        price_history = (
            models.PriceHistory
            .all().ancestor(stock).filter('date', date).get())
        if price_history:
            price_history.close = price
            price_history.volume = volume
        else:
            price_history = models.PriceHistory(
                parent=stock, code=yf.stock, date=date,
                close=price, volume=volume)
        price_history.save()
        return True
    else:
        return False


def update_key_stats(stock, yf):
    # Get key statistics (relies on date collected above)
    stats_data = yf.get_key_stats()
    if stats_data:
        code, eps, roe, bv, pe, mc = stats_data
        per_share = (
            models.PerShare.all().ancestor(stock).filter('date', date).get())
        if not per_share:
            per_share = models.PerShare(parent=stock,
                                        code=yf.stock,
                                        date=date)
            per_share.earnings = eps
            per_share.roe = roe
            per_share.book_value = bv
            per_share.pe = pe
            per_share.market_cap = mc
            per_share.save()


def scrape_yahoo_finance():
    stocks = Detail.objects.filter(is_listed=True)
    for stock in stocks:
        yf = YahooFinance.YahooFinance(stock.key().name())
        update_profile_details(stock, yf)
        if update_latest_price(stock, yf):
            update_key_stats(stock, yf)
    

if __name__ == '__main__':
    scrape_yahoo_finance()
