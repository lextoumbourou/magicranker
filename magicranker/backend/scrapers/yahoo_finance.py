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
    shares_outstanding = attr.attrib()


def get_key_stats(stock, req=None):
    """Return key stats from page HTML."""
    req = req or requests

    url = 'https://finance.yahoo.com/quote/{stock}.AX/key-statistics?p={stock}.AX'.format(
        stock=stock)

    resp = req.get(url)
    if resp.status_code == 404:
        raise StockNotFound(stock)

    soup = BeautifulSoup(resp.content, 'html.parser')
    context = json.loads(
        soup.html.body.find_all('script')[-3].string.split(
            'root.App.main = ', 1)[-1].rsplit(';', 1)[0][:-10])['context']

    financial_data = context['dispatcher']['stores']['QuoteSummaryStore']['financialData']

    roe = (financial_data.get('returnOnEquity') or {}).get('raw')
    roa = (financial_data.get('returnOnAssets') or {}).get('raw')

    key_statistics = context['dispatcher']['stores']['QuoteSummaryStore']['defaultKeyStatistics']

    eps = (key_statistics.get('trailingEps') or {}).get('raw')
    bvps = (key_statistics.get('bookValue') or {}).get('raw')
    shares_outstanding = (key_statistics.get('sharesOutstanding') or {}).get('raw')

    summary_detail = context['dispatcher']['stores']['QuoteSummaryStore']['summaryDetail']

    pe = (summary_detail.get('trailingPE') or {}).get('raw')
    pe = pe if isinstance(pe, float) else None

    market_cap = summary_detail['marketCap'].get('raw')

    return KeyStatsData(
        stock=stock, eps=eps, roe=roe, roa=roa,
        bvps=bvps, pe=pe, market_cap=market_cap, shares_outstanding=shares_outstanding)


def get_current_price(stock, req=None):
    req = req or requests

    url = 'https://finance.yahoo.com/quote/{0}.AX?p={0}.AX'.format(stock)
    resp = req.get(url)

    if resp.status_code == 404:
        raise StockNotFound(stock)

    soup = BeautifulSoup(resp.content, 'html.parser')
    context = json.loads(
        soup.html.body.find_all('script')[-3].string.split(
            'root.App.main = ', 1)[-1].rsplit(';', 1)[0][:-10])['context']

    quote_data = (
        context['dispatcher']['stores'][
            'StreamDataStore']['quoteData']['{0}.AX'.format(stock)])

    # Collect useful data from the CSV
    market_time = quote_data['regularMarketTime']['raw']
    price = quote_data['regularMarketPreviousClose']['raw']
    volume = quote_data['regularMarketVolume']['raw']

    try:
        date = datetime.fromtimestamp(market_time).date()
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
        print("Current price: {current_price}".format(current_price=current_price))
        if current_price:
            print("Key stats {0}".format(get_key_stats(stock)))
