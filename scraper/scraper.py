'''
Scraping classes
'''

import requests
import bs4
import urllib
from selenium import webdriver
import time
import re
#import numpy as np

STORE_DICT = [{'name': 'Tesco',
               'url': 'https://www.tesco.com/',
               'search': 'groceries/en-GB/search?query=',
               'page': 'page='},
              {'name': 'Sainsbury',
               'url': 'https://www.sainsburys.co.uk/',
               'search': 'webapp/wcs/stores/servlet/SearchDisplayView?storeId=10151&searchTerm=',
               'page': 'beginIndex='},
              {'name': 'Asda',
               'url': 'https://groceries.asda.com/',
               'search': 'search/',
               'page': ''},
                {'name': 'Waitrose',
                 'url': 'https://www.waitrose.com/',
                 'search': 'ecom/shop/search?&searchTerm=',
                 'page': ''}
              ]


class Store:
    def __init__(self, store):
        self._name  = store['name']
        self._url   = store['url']
        self._search_url = store['search']
        self._page  = store['page']

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise AttributeError('The `name` attribute cannot be set')

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        raise AttributeError('The `url` attribute cannot be set')

    @property
    def search_url(self):
        return self._search_url

    @search_url.setter
    def search_url(self, value):
        raise AttributeError('The `url` attribute cannot be set')

    @property
    def page(self):
        return self._page

    @page.setter
    def page(self, value):
        raise AttributeError('The `page` attribute cannot be set')


class SearchURL:
    def __init__(self, search_term, store):
        self._search_term = search_term
        self._store       = store
        self._store_name  = store.name
        self._page_num    = 0
        self._url         = ''
        self._error404_counter = 0
        self._page_limit  = 2
        self._items       = []

    @property
    def search_term(self):
        return self._search_term

    @search_term.setter
    def search_term(self, value):
        self._search_term = value

    @property
    def store(self):
        return self._store

    @store.setter
    def store(self, value):
        self._store = value

    @property
    def page_num(self):
        return self._page_num

    @page_num.setter
    def page_num(self, value):
        if ((type(value) != int) or (value < 0)):
            raise ValueError('`page_num` attribute should be integer and larger than 0!')
        self._page_num = value

    def make_new_url(self):
        self.url = urllib.parse.urljoin(self.store.url, self.store.search_url)
        self.url = self.url + self.search_term + '&' + self.store.page + str(self.page_num)

    def start_collecting_data(self):
        while self.page_num < self._page_limit and self._error404_counter < 2:
            self.make_new_url()
            res = self.request_url()
            if res != -1:
                self._items.extend(res)
            self.page_num += 1

    def request_url(self):
        r = requests.get(self.url)
        if r.status_code == 404:
            print('error 404')
            self._error404_counter += 1
            return -1
        else:
            print('starting get_details ' + self.store.name)
            self._error404_counter = 0
            return self.get_details(r)

    def get_details(self, r):
        print('get_details in SearchURL')
        return bs4.BeautifulSoup(r.text)


class Tesco(SearchURL):
    def __init__(self, search_term, store):
        SearchURL.__init__(self, search_term=search_term, store=store)

    def get_details(self, r):
        print('get_details in Tesco class')
        bso = bs4.BeautifulSoup(r.text, 'html.parser')
        items = bso.findAll('div', attrs={'class': 'tile-content'})
        details = []
        for num, it in enumerate(items):
            details.append(self.get_item_information(it))
        return details

    def get_item_information(self, item):
        contain = {}
        contain['store_name'] = self.store.name
        contain['address'] = urllib.parse.urljoin(self.store.url, item.find('a')['href'])
        try:
            contain['name'] = item.find('a', attrs={'class': 'product-tile--title product-tile--browsable'}).text.strip()
        except AttributeError:
            contain['name'] = ''
        try:
            img = item.find('img')
            contain['image'] = img['src']
        except AttributeError:
            contain['image'] = ''
        try:
            contain['price'] = item.find('div', attrs={'class': 'price-control-wrapper'}).text.strip()
        except AttributeError:
            contain['price'] = ''#np.nan
        try:
            contain['unit price'] = item.find('div', attrs={'class': 'price-per-quantity-weight'}).text.strip()
        except AttributeError:
            contain['unit price'] = ''#np.nan
        try:
            prom = item.find('div', attrs={'class': 'list-item-content promo-content-small'})
            contain['promotion'] = ' '.join([x.text for x in prom.findAll('span')])
        except AttributeError:
            contain['promotion'] = ''
        return contain


class Sainsbury(SearchURL):
    def __init__(self, search_term, store):
        SearchURL.__init__(self, search_term=search_term, store=store)

    def get_details(self, r):
        bso = bs4.BeautifulSoup(r.text, 'html.parser')
        grid = bso.find('div', attrs={'class': 'section', 'id':'productsContainer'})
        items = grid.findAll('li', attrs={'class': 'gridItem'})
        details = []
        for num, it in enumerate(items):
            details.append(self.get_item_information(it))
        return details

    def get_item_information(self, item):
        contain = {}
        contain['store_name'] = self.store.name
        contain['address'] = item.find('a')['href']
        try:
            contain['name'] = item.find('a').text.strip()
        except AttributeError:
            contain['name'] = ''
        try:
            img = item.find('img')
            contain['image'] = img['src']
        except AttributeError:
            contain['image'] = ''
        try:
            contain['price'] = item.find('p', attrs={'class': 'pricePerUnit'}).text.strip()
        except AttributeError:
            contain['price'] = ''#np.nan
        try:
            contain['unit price'] = item.find('p', attrs={'class': 'pricePerMeasure'}).text.strip()
        except AttributeError:
            contain['unit price'] = ''#np.nan
        try:
            prom = item.find('div', attrs={'class': 'promotion'})
            contain['promotion'] = prom.p.a.text.strip()
        except AttributeError:
            contain['promotion'] = ''
        return contain


class Asda(SearchURL):
    def __init__(self, search_term, store):
        SearchURL.__init__(self, search_term=search_term, store=store)
        self.driver = driver = webdriver.PhantomJS()

    def make_new_url(self):
        self.url = urllib.parse.urljoin(self.store.url, self.store.search_url)
        self.url = self.url + self.search_term

    def get_details(self, r):
        self.driver.get(self.url)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/1.5);")
        time.sleep(1)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/1.1);")
        time.sleep(1)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        bso = bs4.BeautifulSoup(self.driver.page_source, 'html.parser')
        grid = bso.findAll('div', id=lambda x: x and x.startswith('listingsContainer'))
        details = []

        for gr in grid:
            items = gr.findAll('div', attrs={'class': 'product-content'})
            for num, it in enumerate(items):
                details.append(self.get_item_information(it))
        return details

    def get_item_information(self, item):
        contain = {}
        contain['store_name'] = self.store.name
        contain['address'] = urllib.parse.urljoin(self.store.url, item.find('a')['href'])
        try:
            contain['name'] = item.find('a').text.strip()
        except AttributeError:
            contain['name'] = ''
        try:
            xx = item.find('span', attrs={'class': 'price'})
            contain['price'] = xx.findAll('span')[-1].text.strip()
        except AttributeError:
            contain['price'] = ''#np.nan
        try:
            img = item.parent.find('img')
            contain['image'] = img['src']
        except:
            contain['image'] = ''
        try:
            unit_price = item.find('span', attrs={'class': 'priceInformation'}).text.strip()
            unit_price = unit_price.replace('(', '')
            unit_price = unit_price.replace(')', '')
            contain['unit price'] = unit_price
        except AttributeError:
            contain['unit price'] = ''#np.nan
        try:
            prom = item.find('span', attrs={'class': 'linksave'})
            contain['promotion'] = prom.text.strip()
        except AttributeError:
            contain['promotion'] = ''
        return contain


class Waitrose(SearchURL):
    def __init__(self, search_term, store):
        SearchURL.__init__(self, search_term=search_term, store=store)
        self.driver = webdriver.PhantomJS()

    def make_new_url(self):
        self.url = urllib.parse.urljoin(self.store.url, self.store.search_url)
        self.url = self.url + self.search_term

    def get_details(self, r):
        self.driver.get(self.url)
        bso = bs4.BeautifulSoup(self.driver.page_source, 'html.parser')
        items = bso.findAll('article', attrs={'data-test':'product-pod'})
        details = []
        for num, it in enumerate(items):
            details.append(self.get_item_information(it))
        return details

    def get_item_information(self, item):
        contain = {}
        contain['store_name'] = self.store.name
        contain['address'] = urllib.parse.urljoin(self.store.url, item.header.a['href'])
        try:
            contain['name'] = item.header.span.text.strip()
        except AttributeError:
            contain['name'] = ''
        try:
            img = item.find('picture')
            contain['image'] = img.div.img['src']
        except AttributeError:
            contain['image'] = ''
        price_tag = item.find('div', {'class': re.compile(r'prices')})
        try:
            contain['price'] = price_tag.span.span.text.strip()
        except AttributeError:
            contain['price'] = ''#np.nan
        try:
            unit_price = price_tag.findAll('span')[-1].text
            unit_price = re.match(r'.*\((.*)\)', unit_price)
            contain['unit price'] = unit_price.group(1)
        except AttributeError:
            contain['unit price'] = ''#np.nan
        try:
            prom = item.find('span', {'class': re.compile(r'offerDescription')})
            contain['promotion'] = prom.text.strip()
        except AttributeError:
            contain['promotion'] = ''
        return contain

def init_stores(db):
    return [Store(st) for st in db]

STORE_MAP = {'Tesco': Tesco,
             'Sainsbury': Sainsbury,
             'Asda': Asda,
             'Waitrose': Waitrose
             }


if __name__ == '__main__':
    store_list = init_stores(STORE_DICT)
    prod_collect = []
    for st in store_list:
        class2call = STORE_MAP.get(st.name)
        prod_info = class2call('milk', st)
        prod_info.start_collecting_data()
        prod_collect.extend(prod_info._items)
