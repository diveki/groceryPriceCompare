

import requests
import bs4
import urllib
from selenium import webdriver
import time
import re

from store_classes import *

STORE_DICT_UK = [{'name': 'Tesco',
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

STORE_MAP_UK = {'Tesco': Tesco,
             'Sainsbury': Sainsbury,
             'Asda': Asda,
             'Waitrose': Waitrose
             }
