'''
Scraping classes
'''

import requests
import bs4
import urllib
#import numpy as np

STORE_DICT = [{'name': 'Tesco',
               'url': 'https://www.tesco.com/',
               'search': 'groceries/en-GB/search?query=',
               'page': 'page='},
              {'name': 'Sainsbury',
               'url': 'https://www.sainsburys.co.uk/',
               'search': 'webapp/wcs/stores/servlet/SearchDisplayView?storeId=10151&searchTerm=',
               'page': 'beginIndex='}
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
        self._page_limit  = 3
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
            print('starting get_details')
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
        bso = bs4.BeautifulSoup(r.text)
        items = bso.findAll('div', attrs={'class': 'tile-content'})
        details = []
        for num, it in enumerate(items):
            details.append(self.get_item_information(it))
        return details

    def get_item_information(self, item):
        cont = {}
        cont['store_name'] = self.store.name
        cont['address'] = urllib.parse.urljoin(self.store.url, item.find('a')['href'])
        try:
            cont['name'] = item.find('a', attrs={'class': 'product-tile--title product-tile--browsable'}).text.strip()
        except AttributeError:
            cont['name'] = ''
        try:
            cont['price'] = item.find('div', attrs={'class': 'price-control-wrapper'}).text.strip()
        except AttributeError:
            cont['price'] = ''#np.nan
        try:
            cont['unit price'] = item.find('div', attrs={'class': 'price-per-quantity-weight'}).text.strip()
        except AttributeError:
            cont['unit price'] = ''#np.nan
        try:
            prom = item.find('div', attrs={'class': 'list-item-content promo-content-small'})
            cont['promotion'] = ' '.join([x.text for x in prom.findAll('span')])
        except AttributeError:
            cont['promotion'] = ''
        return cont


class Sainsbury(SearchURL):
    def __init__(self, search_term, store):
        SearchURL.__init__(self, search_term=search_term, store=store)

    def get_details(self, r):
        bso = bs4.BeautifulSoup(r.text)
        grid = bso.find('div', attrs={'class': 'section', 'id':'productsContainer'})
        items = grid.findAll('li', attrs={'class': 'gridItem'})
        details = []
        for num, it in enumerate(items):
            details.append(self.get_item_information(it))
        return details

    def get_item_information(self, item):
        cont = {}
        cont['store_name'] = self.store.name
        cont['address'] = item.find('a')['href']
        try:
            cont['name'] = item.find('a').text.strip()
        except AttributeError:
            cont['name'] = ''
        try:
            cont['price'] = item.find('p', attrs={'class': 'pricePerUnit'}).text.strip()
        except AttributeError:
            cont['price'] = ''#np.nan
        try:
            cont['unit price'] = item.find('p', attrs={'class': 'pricePerMeasure'}).text.strip()
        except AttributeError:
            cont['unit price'] = ''#np.nan
        try:
            prom = item.find('div', attrs={'class': 'promotion'})
            cont['promotion'] = prom.p.a.text.strip()
        except AttributeError:
            cont['promotion'] = ''
        return cont


def init_stores(db):
    return [Store(st) for st in db]

STORE_MAP = {'Tesco': Tesco,
             'Sainsbury': Sainsbury}


if __name__ == '__main__':
    store_list = init_stores(STORE_DICT)
    prod_collect = []
    for st in store_list:
        class2call = STORE_MAP.get(st.name)
        prod_info = class2call('milk', st)
        prod_info.start_collecting_data()
        prod_collect.extend(prod_info._items)
