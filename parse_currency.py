#!/usr/bin/python
import sys
import json
import requests
from bs4 import BeautifulSoup


class AbstractCurrencyParser(object):

    def __init__(self, base_currency, url):
        """Designated initialization.
        Args:
            base_currency: is the base currency used in exchange rate of
            other currencies
            url: is where the information of exchange rate located
        """
        self.base_currency = base_currency
        self.url = url

    def process(self):
        """Start fetching and parsing the exchange rate
        information on the url
        """
        html = self.fetchHTML(self.url)
        sys.stdout.write("="*36 + '%s\n' % self + 'Start parsing:\n')
        self.parseHTML(html)

    def fetchHTML(self, url):
        """Fetching the html content from the url, and
        will return the html content
        """
        r = requests.get(url)
        return r.text

    def parseHTML(self, html):
        """Will parse the html content, and get the exchange
        rates information
        """
        raise NotImplementedError(
            "This method must be implemented on subclass"
        )

    def __repr__(self):
        """The string representation of the object."""
        res = '\nCurrency: {}\nURL: {}'.format(self.base_currency, self.url)
        return res


class KursComUAParser(AbstractCurrencyParser):
    """Currency rate parser from kurs.com.ua"""

    def __init__(self):
        self.base_currency = 'UAH'
        self.url = 'http://kurs.com.ua/ajax/main_table/all/13.03.2016/all'
        self.codes_list = []
        self.buy_list = []
        self.sale_list = []

    def parseHTML(self, html):
        json_data = json.loads(html)

        html_table = json_data['table']
        soup = BeautifulSoup(html_table, 'html.parser')

        self.parse_list_currency(soup)
        self.parse_sale_and_buy(soup)

        return self.conclude()

    def parse_list_currency(self, soup):
        """Parse currency codes"""

        all_rows = soup.find_all('td', {'class': 'column_1'})

        for row in all_rows:
            self.codes_list.append(
                row.find_all("div", "value")[0].find_next().get_text().strip()
            )

    def parse_sale_and_buy(self, soup):
        """Parse sale and buy prices"""

        all_rows = soup.find_all('tr', {'class': 'regular'})
        for row in all_rows:
            buy = row.find_all('td', {'class': 'column_2'})[0].find_all(
                "div", "value")[0].find_next().get_text().strip()
            buy = format(float(buy), '.5f')

            sale = row.find_all('td', {'class': 'column_3'})[0].find_all(
                    "div", "value")[0].find_next().get_text().strip()
            sale = format(float(sale), '.5f')

            self.buy_list.append(buy)
            self.sale_list.append(sale)

    def conclude(self):
        """Write result to stdout"""

        stdout = '{:^8} {:^14} {:^14}\n'.format(*('CODE', 'BUY', 'SELL'))
        sys.stdout.write(stdout)
        sys.stdout.write("="*36 + '\n')
        data = zip(self.codes_list, self.buy_list, self.sale_list)
        for item in data:
            sys.stdout.write('{:^8} {:^14} {:^14}\n'.format(*item))


class Privat24Parser(KursComUAParser):
    """Currency rate parser from Privat24 API"""
    def __init__(self):
        super(Privat24Parser, self).__init__()
        url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&'
        url += 'coursid=11'
        self.url = url

    def parseHTML(self, html):
        json_data = json.loads(html)
        self.parce_json_data(json_data)
        return self.conclude()

    def parce_json_data(self, data):
        """Parse currency codes, sale and buy prices"""
        for item in data:
            self.codes_list.append(item.get('ccy'))
            self.buy_list.append(item.get('buy'))
            self.sale_list.append(item.get('sale'))


if __name__ == "__main__":

    parser1 = KursComUAParser()
    parser1.process()

    parser2 = Privat24Parser()
    parser2.process()
