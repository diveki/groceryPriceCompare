import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scraper'))

from scraper import *
import pandas as pd

class SearchResult:
    def __init__(self, data):
        self.transform_data(data)

    def transform_data(self, data):
        for store in data:
            for page in store:
                for num, item in page.items():
                    import pdb
                    pdb.set_trace()


if __name__ == '__main__':
    store_list = init_stores(STORE_DICT)
    prod_collect = []
    for st in store_list:
        class2call = STORE_MAP.get(st.name)
        prod_info = class2call('milk', st)
        prod_info.start_collecting_data()
        prod_collect.append(prod_info._items)

    df = SearchResult(prod_collect)
