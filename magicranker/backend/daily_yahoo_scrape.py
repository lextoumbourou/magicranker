from datetime import datetime, timedelta
from scrapers import YahooFinance

from stock.models import Detail


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


def main():
    stocks = Detail.objects.filter(is_listed=True)
    for stock in stocks:
        yf = YahooFinance.YahooFinance(stock.key().name())
        update_profile_details(stock, yf)
        if update_latest_price(stock, yf):
            update_key_stats(stock, yf)


if __name__ == '__main__':
    main()
    


