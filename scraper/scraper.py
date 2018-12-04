'''
Scraping classes
'''

import requests
import bs4

STORE_DICT = [{'name': 'Tesco',
               'url': 'https://www.tesco.com/groceries/en-GB/search?query=',
               'page': 'page='},
              {'name': 'Sainsbury',
               'url': 'https://www.sainsburys.co.uk/webapp/wcs/stores/servlet/SearchDisplayView?storeId=10151&searchTerm=',
               'page': 'beginIndex='}
              ]


class Store:
    def __init__(self, store):
        self._name  = store['name']
        self._url   = store['url']
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
    def page(self):
        return self._page

    @page.setter
    def page(self, value):
        raise AttributeError('The `page` attribute cannot be set')


class SearchURL:
    def __init__(self, search_term, store):
        self._search_term = search_term
        self._store       = store
        self._page_num    = 0
        self._url = ''

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
        self.url = self.store.url + self.search_term + '&' + self.store.page + str(self.page_num)
        self.page_num += 1



def init_stores(db):
    return [Store(st) for st in db]


if __name__ == '__main__':
    store_list = init_stores(STORE_DICT)
    print(store_list)
