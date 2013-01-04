import re
import csv
from StringIO import StringIO

import utils


def get_full_stock_list():
    """
    Gets the full list of stocks from ASX
    """
    stock_list = []
    asx_companies = utils.get_page(
        'http://www.asx.com.au/asx/research/ASXListedCompanies.csv')
    if asx_companies:
        csvfile = csv.reader(StringIO(asx_companies), delimiter=',')
        for row in csvfile:
            # Skip the rows without CSV data
            if len(row) <= 1:
                continue
            # Check if CSV is a 3-letter stock code
            if re.search(r'^\w\w\w$', row[1]):
                stock_list.append(row[1])
            else:
                pass
        return stock_list
    else:
        return None

if __name__ == '__main__':
    print get_full_stock_list()
