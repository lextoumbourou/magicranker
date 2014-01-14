import urllib2
import datetime as dt
import csv
import re
import time
import logging
from datetime import datetime
from urllib import urlencode

import HTMLParser

from BeautifulSoup import BeautifulSoup
import requests
import utils


def format_title(title):
    title = re.sub(r'(\&nbsp\;|\,|\n|\-|\')', '', str(title).strip())
    # Replace the space with an underscore
    title = re.sub(r'(\ |\/)', '_', str(title.lower()))
    return title


def get_title_from_top_row(tr):
    # Get all the <td>s in the <tr>
    td = tr.findAll('td')
    # If it's a bolded piece, follow these instructions
    try:
        title = td[0].strong.string
        title = format_title(title)
        return title
    except:
        pass
    # If it's a bolded piece, follow these instructions
    try:
        title = td[0].string
        title = format_title(title)
        return title
    except:
        pass


def get_title_from_indent_row(tr):
    # Get all the <td>s in the <tr>
    td = tr.findAll('td')
    # If it's a bolded piece, follow these instructions
    try:
        title = td[1].string
        title = format_title(title)
        return title
    except:
        pass


def get_list_from_row(tr):
    output = []
    td = tr.findAll('td')
    for t in td:
        try:
            data = t.strong.string
        except:
            data = t.string
        data = re.sub(r'(\&nbsp\;|\,|\n|\/|\')', '', str(data).strip())
        # If data is a negative number, change format
        if re.search(r'\(|\)', data):
            data = re.sub(r'\(|\)', '', data)
            data = '-' + data
        # If Data is a number or a dash add to list
        if re.search(r'(\d+)', data):
            output.append(data)
        elif re.search(r'(-)', data):
            output.append(None)

    return output


class YahooFinance():
    def __init__(self, stock):
        self.stock = stock

    def get_current_price(self):
        """
        Save the open and close price to the database
        """
        url = 'http://download.finance.yahoo.com/d'
        url += '/quotes.csv?s={0}.AX&f=sl1d1t1c1ohgv&e=.csv'.format(self.stock)
        page = utils.get_page(url)
        values = None
        if page:
            values = page.split(',')

        if not values:
            return False

        # Collect useful data from the CSV
        date_string = values[2]
        price = values[6]
        volume = values[8]

        # Convert date to datetime object
        try:
            self.date = datetime.strptime(date_string, '"%m/%d/%Y"').date()
        except ValueError:
            return False

        try:
            price = float(price)
        except ValueError:
            price = 0

        try:
            volume = int(volume)
        except ValueError:
            volume = 0

        return (self.stock, self.date, price, volume)

    def get_profile(self):
        """
        Gets the company title and description
        @returns dict
        """
        h = HTMLParser.HTMLParser()
        # Get the page data
        url = 'http://finance.yahoo.com/q/'
        url += 'pr?s={0}.AX+Profile'.format(self.stock)
        page = utils.get_page(url)
        soup = BeautifulSoup(page)

        # Attempt to scrape the title
        data = soup.find('div', 'title')
        try:
            name = h.unescape(data.h2.string)
        except (AttributeError, IndexError), error:
            logging.info(
                "Couldn't find a title for {0}".format(self.stock))
            logging.error(error)
            name = ''
        name = str(re.sub(r'(\ \(\w\w\w\.\w\w\))', '', name))

        # Now, scrape the description
        try:
            description = soup.findAll('p')[3].string
            if not description:
                description = ''
        except (AttributeError, IndexError), error:
            logging.info(
                "Couldn't find a description for {0}".format(self.stock))
            logging.error(error)
            description = ''

        return (self.stock, name, description)

    def get_key_stats(self):
        """
        Get earnings per share, roe, book value, pe and market cap
        and return as tuple
        """
        url = 'http://finance.yahoo.com/q/'
        url = url + 'ks?s={0}.AX+Key+Statistics'.format(self.stock)
        content = utils.get_page(url)
        soup = BeautifulSoup(''.join(str(content)))

        values = soup.findAll('td', 'yfnc_tabledata1')

        # Get Market Cap
        try:
            market_cap = values[0].span.string
            # Remove the M or B for market cap
            if re.search(r'M$', market_cap):
                market_cap = re.sub(r'M', '', market_cap)
                # Now that the M is removed,
                # multiply it by a million to get the actual value
                market_cap = float(market_cap)*1000000
            elif re.search(r'B$', market_cap):
                market_cap = re.sub(r'B', '', market_cap)
                # Now that the B is removed,
                # multiply it by a million to get the actual value
                market_cap = float(market_cap)*1000000000
            elif re.search(r'K$', market_cap):
                market_cap = re.sub(r'K', '', market_cap)
                # Now that the K is removed,
                # multiply by a million to get the actual value
                market_cap = float(market_cap)*1000
        except:
            market_cap = None

        # Get PE
        try:
            pe = float(values[2].string)
        except (ValueError, IndexError):
            pe = None

        # Get ROE
        try:
            roe = values[14].string
            # Remove the percent and convert to a fraction
            roe = re.sub(r'\%', '', roe)
            roe = float(roe)/100
        except (ValueError, IndexError):
            roe = None

        # Get Earnings
        try:
            eps = values[21].string
            eps = float(eps)
        except:
            eps = None

        # Get Book Value Per Share
        try:
            bvps = float(values[28].string)
        except (ValueError, IndexError):
            bvps = None

        return (self.stock, eps, roe, 
                bvps, pe, market_cap,)

    def _get_all_assets(self, trs):
        """
        Get all assets
        """
        output = {}
        # Current assets
        for tr in trs[4:9]:
            title = get_title_from_indent_row(tr)
            output[title] = []
            output[title] = get_list_from_row(tr)

            # Total current assets
            title = get_title_from_top_row(trs[10])
            output[title] = []
            output[title] = get_list_from_row(trs[10])

            # Total assets fields
            for tr in trs[11:17]:
                title = get_title_from_top_row(tr)
                output[title] = []
                output[title] = get_list_from_row(trs[10])

                ## Total of the total assets
                title = get_title_from_top_row(trs[19])
                output[title] = []
                output[title] = get_list_from_row(trs[19])

        return output

    def _get_all_liabilities(self, trs):
        """
        Get all liabilities
        """
        output = {}
        # Current liabilites
        for tr in trs[23:26]:
                title = get_title_from_indent_row(tr)
                output[title] = []
                output[title] = get_list_from_row(tr)

        # Get Total Current Liabilities
        title = get_title_from_top_row(trs[27])
        output[title] = []
        output[title] = get_list_from_row(trs[27])

        for tr in trs[28:33]:
                title = get_title_from_top_row(tr)
                output[title] = []
                output[title] = get_list_from_row(tr)

        title = get_title_from_top_row(trs[34])
        output[title] = []
        output[title] = get_list_from_row(trs[34])
        return output

    def get_bal_sheet(self):
        """
        Get balance sheet data
        """
        output = {}
        url = 'http://finance.yahoo.com/q/'
        url += 'bs?s={0}.AX+Balance+Sheet&annual'.format(self.stock.code)

        try:
            soup = BeautifulSoup(utils.get_page(url))
        except:
            print "HTTP Request failed. Skipping."
            return False

        try:
            dates_html = soup.findAll('td', "yfnc_modtitle1")
            date_title = dates_html[0].small.span.string
            # Convert to lowercase and replace spaces with underscores
            date_title = re.sub(r'(\ )', '_', str(date_title.lower()))
        except:
            print 'Failed to get date range. Skipping.'
            return False
        output[date_title] = []
        # Get all dates
        for date in dates_html[1:5]:
            # Get the string from the HTML (the text is in a <b> tag)
            # and convert to a valid time format
            date = str(date.b.string)
            date = time.strptime(date, "%b %d, %Y")
            date = time.strftime("%Y-%m-%d", date)
            output[date_title].append(date)

        # Get the rest of the page data by first grabbing the main table,
        # then the <tr>s in that
        trs = (soup.find('table', 'yfnc_tabledata1')
                   .find('table')
                   .findAll('tr'))
        output.update(self._get_all_assets(trs))
        output.update(self._get_all_liabilities(trs))
        return output 

    def get_price_history(self):
        """Return the price history for the company as a list of lists"""
        today = dt.datetime.today()

        if self.stock.startswith('^'):
            stock = self.stock
        else:
            stock = self.stock + '.AX'

        url = (
            'http://ichart.finance.yahoo.com/'
            'table.csv?s={0}&a=00&b=1&c=1900'
            '&d={1}&e={2}&f={3}&g=d&ignore=.csv').format(
                self.stock, today.day, today.month, today.year)
        print url
        response = requests.get(url)

        if response.status_code == 200:
            return csv.reader(response.content.split('\n'), delimiter=',')


if __name__ == '__main__':
    for stock in ['^AXJO', 'ANZ', 'CBA']:
        y = YahooFinance(stock)
        y.get_profile()
        if y.get_current_price():
            y.get_key_stats()
        print [r for r in y.get_price_history()]
