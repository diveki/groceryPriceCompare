

import requests
import bs4
import urllib
from selenium import webdriver
import time
import re

from store_classes import *


STORE_DICT_HU = [{'name': 'Tesco',
               'url': 'https://bevasarlas.tesco.hu/',
               'search': 'groceries/en-GB/search?query=',
               'page': 'page='}
                   ]

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
        contain['address'] = urllib.parse.urljoin(self.store.url, item.find('a', attrs={'class': re.compile(r'product-tile--')})['href'])
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



STORE_MAP_HU = {'Tesco': Tesco
             }
