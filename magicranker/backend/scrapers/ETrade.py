import sys
import os
import urllib
import urllib2
import re
import ssl
import StringIO

import pycurl
from BeautifulSoup import BeautifulSoup


USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0.1)'
USER_AGENT += 'Gecko/20100101 Firefox/4.0.1'


class ETrade():
    def __init__(self):
        self.user_agent = USER_AGENT
        self.headers = {'User-Agent': USER_AGENT,
                        'Content-Type': 'application/x-www-form-urlencoded'}
        self.cookie_path = '/tmp/cookies'

    def login(self, username, password):
        post_data = {'Login1$CookiesEnabled': '',
                     'Login1$HiddenDate': '',
                     'Login1$ddlStartIn': '/Login.aspx',
                     'Login1$txtPassword': password,
                     'Login1$txtUserName': username,
                     'TitleBar1$ctl02$GlobalQuote': '',
                     '__EVENTARGUMENT': 'Click',
                     '__EVENTTARGET': 'Login1$btnLogin',
                     '__VIEWSTATE': '',
                     '__VIEWSTATE_ID': '3',
                     'txtAnalyticsPageName': 'VISITOR/Home/',
                     'txtAnalyticsPageNameManual': 'generic'}
        post_data = urllib.urlencode(post_data)
        b = StringIO.StringIO()
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, 'https://invest.etrade.com.au/Login.aspx')
        curl.setopt(pycurl.USERAGENT, self.user_agent),
        curl.setopt(pycurl.POST, 1)
        curl.setopt(pycurl.POSTFIELDS, post_data)
        curl.setopt(pycurl.FOLLOWLOCATION, 1)
        curl.setopt(pycurl.SSL_VERIFYPEER, False)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        curl.setopt(pycurl.REFERER, 'https://invest.etrade.com.au/Home.aspx')
        curl.setopt(pycurl.COOKIEFILE, self.cookie_path)
        curl.setopt(pycurl.COOKIEJAR, self.cookie_path)
        curl.setopt(pycurl.WRITEFUNCTION, b.write)
        curl.perform()
        if curl.getinfo(pycurl.HTTP_CODE) == '200':
            print 'Login successful'
            c.close()

    def _get_page(self, stock):
        url = 'https://invest.etrade.com.au/QuotesAndResearch/Shares/'
        url += 'Profile.aspx?symbol={0}&tab=Balance%20Sheet'.format(
            stock.code)
        b = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL, str(url))
        c.setopt(pycurl.USERAGENT, self.user_agent),
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.SSL_VERIFYPEER, False)
        c.setopt(pycurl.SSL_VERIFYHOST, 0)
        c.setopt(pycurl.REFERER, url)
        c.setopt(pycurl.COOKIEFILE, self.cookie_path)
        c.setopt(pycurl.COOKIEJAR, self.cookie_path)
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        c.perform()
        return b.getvalue()

    def _clean_html(self, page):
        """
        Remove some ugly syntax in the HTML code so B.S.
        doesn't break and convert tags to lower case
        """
        page = re.sub("scr'\+'ipt", 'script', page, flags=re.IGNORECASE)
        page = re.sub(r'<TD', "<td", page)
        page = re.sub(r'<\/TD', "<\/td", page)

        return page

    def _get_dates(self, trs):
        output = []
        for tr in trs:
            for td in tr.findAll('td'):
                try:
                    content = td.b.string
                except AttributeError:
                    content = ''
                if re.search(r'(\d{4}/\d{2})', content):
                    date = '{0}-{1}-01'.format(
                        content.split('/')[0], content.split('/')[1])
                    output.append(date)
        return output

    def _get_values(self, trs, value_name):
        output = []
        for tr in trs:
            try:
                title = tr.findAll('td')[0].string
            except AttributeError:
                title = ''

            if title == value_name:
                for td in tr.findAll('td')[1:]:
                    try:
                        value = td.string
                        value = re.sub(r',', '', value)
                        if value == '--':
                                value = None
                        output.append(value)
                    except:
                        pass

        return output

    def get_data(self, stock):
        data = {}
        page = str(self._get_page(stock))
        if page:
            page = self._clean_html(page)
            soup = BeautifulSoup(page)
            # Last table should have ROE in it
            try:
                trs = soup.findAll('table', rules='all')[-1].findAll('tr')
            except:
                print "Ignoring this stock"
                return False

            data['periods'] = self._get_dates(trs)
            data['roe'] = self._get_values(trs, 'Return on equity (%)')

            # Get 3rd last table (should have Per Share stats in it)
            try:
                trs = soup.findAll('table', rules='all')[-2].findAll('tr')
            except:
                print "Ignoring this stock"
                return False

            data['shares_out'] = self._get_values(
                trs, 'Shares Outstanding (m)')
            data['book_value'] = self._get_values(trs, 'Book Value ($)')
            data['earnings'] = self._get_values(trs, 'Earnings (cents)')
            data['pe'] = self._get_values(trs, 'Avg P/E Ratio')

        return data
