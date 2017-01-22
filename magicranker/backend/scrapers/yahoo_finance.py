from datetime import datetime

import attr
import requests


class StockNotFound(Exception):

    """Raise when stock not found."""

    pass


@attr.attrs
class PriceData(object):

    """Represents price data returned from Yahoo Finance."""

    stock = attr.attrib()
    date = attr.attrib()
    close = attr.attrib()
    volume = attr.attrib()


@attr.attrs
class KeyStatsData(object):

    """Represents key stats data returned from Yahoo Finance."""

    stock = attr.attrib()
    eps = attr.attrib()
    roe = attr.attrib()
    roa = attr.attrib()
    bvps = attr.attrib()
    pe = attr.attrib()
    market_cap = attr.attrib()


def get_key_stats(stock, req=None):
    """Return key stats from page HTML."""
    req = req or requests

    url = (
        'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{0}.AX?'
        'formatted=true&lang=en-US&region=AU&'
        'modules=summaryDetail,defaultKeyStatistics,financialData,'
        'calendarEvents&corsDomain=finance.yahoo.com').format(stock)
    resp = req.get(url)
    if resp.status_code == 404:
        raise StockNotFound(stock)

    try:
        data = resp.json()
    except ValueError:
        raise StockNotFound(stock)

    if (
        data['quoteSummary'].get('error') and
        data['quoteSummary']['error']['code'] == 'Not Found'
    ):
        raise StockNotFound(stock)

    financial_data = data['quoteSummary']['result'][0]['financialData']

    roe = financial_data['returnOnEquity'].get('raw')
    roa = financial_data['returnOnAssets'].get('raw')

    key_statistics = data['quoteSummary']['result'][0]['defaultKeyStatistics']

    eps = key_statistics['trailingEps'].get('raw')
    bvps = key_statistics['bookValue'].get('raw')

    summary_detail = data['quoteSummary']['result'][0]['summaryDetail']

    pe = summary_detail['trailingPE'].get('raw')
    pe = pe if isinstance(pe, float) else None

    market_cap = summary_detail['marketCap'].get('raw')

    return KeyStatsData(
        stock=stock, eps=eps, roe=roe,
        roa=roa, bvps=bvps, pe=pe, market_cap=market_cap)


def get_current_price(stock, req=None):
    req = req or requests
    url = (
        'http://download.finance.yahoo.com/d'
        '/quotes.csv?s={0}.AX&f=sl1d1t1c1ohgv&e=.csv'.format(stock))
    r = req.get(url)
    page = r.text

    values = None
    if page:
        values = page.split(',')

    if not values:
        return False

    # Collect useful data from the CSV
    date_string = values[2]
    price = values[6]
    volume = values[8]

    try:
        date = datetime.strptime(date_string, '"%m/%d/%Y"').date()
    except ValueError:
        return False

    try:
        price = float(price)
    except ValueError:
        price = None

    try:
        volume = int(volume)
    except ValueError:
        volume = None

    return PriceData(stock=stock, date=date, close=price, volume=volume)


if __name__ == '__main__':
    for stock in ['ANZ', 'CBA']:
        current_price = get_current_price(stock)
        print "Current price", current_price
        if current_price:
            print "Key stats", get_key_stats(stock)
