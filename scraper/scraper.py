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


from scraper_uk import *
from scraper_hu import *


def init_stores(db):
    return [Store(st) for st in db]


STORE_DICT = {
        'UK': STORE_DICT_UK,
        'HU': STORE_DICT_HU
}

STORE_MAP = {
        'UK': STORE_MAP_UK,
        'HU': STORE_MAP_HU
}

if __name__ == '__main__':
    store_list = init_stores(STORE_DICT['UK'])
    prod_collect = []
    for st in store_list:
        class2call = STORE_MAP['UK'].get(st.name)
        prod_info = class2call('milk', st)
        prod_info.start_collecting_data()
        prod_collect.extend(prod_info._items)
