import csv
from io import StringIO

import attr
import requests


@attr.attrs
class StockData(object):

    name = attr.attrib()
    code = attr.attrib()
    category = attr.attrib()


def get_full_stock_list(req=None):
    """
    Gets the full list of stocks from ASX
    """
    req = req or requests
    r = requests.get(
        'http://www.asx.com.au/asx/research/ASXListedCompanies.csv')
    asx_companies = r.text

    csvfile = csv.reader(StringIO(asx_companies), delimiter=',')

    for row in csvfile:
        # Skip the rows without CSV data
        if len(row) <= 1:
            continue

        yield StockData(name=row[0].title(), code=row[1], category=row[2])


if __name__ == '__main__':
    for stock in get_full_stock_list():
        print(stock)
