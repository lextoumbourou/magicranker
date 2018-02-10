import json
from datetime import datetime

from bs4 import BeautifulSoup

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

    url = f'https://finance.yahoo.com/quote/{stock}.AX/key-statistics?p={stock}.AX'

    resp = req.get(url)
    if resp.status_code == 404:
        raise StockNotFound(stock)

    soup = BeautifulSoup(resp.content, 'html.parser')
    context = json.loads(
        soup.html.body.find_all('script')[-3].string.split('root.App.main = ', 1)[-1].rsplit(';', 1)[0][:-10])['context']

    financial_data = context['dispatcher']['stores']['QuoteSummaryStore']['financialData']

    roe = financial_data['returnOnEquity'].get('raw')
    roa = financial_data['returnOnAssets'].get('raw')

    key_statistics = context['dispatcher']['stores']['QuoteSummaryStore']['defaultKeyStatistics']

    eps = key_statistics['trailingEps'].get('raw')
    bvps = key_statistics['bookValue'].get('raw')

    summary_detail = context['dispatcher']['stores']['QuoteSummaryStore']['summaryDetail']

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
        print("Key stats {0}".format(get_key_stats(stock)))
