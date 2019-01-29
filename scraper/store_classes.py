
import requests
import bs4
import urllib
from selenium import webdriver
import time
import re


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
