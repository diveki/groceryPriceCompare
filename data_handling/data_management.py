import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scraper'))

from scraper import *
import pandas as pd
import numpy as np

class SearchResult:
    def __init__(self, data):
        self.transform_data(data)

    def transform_data(self, data):
        hold_dict = {key: [] for key, value in data[0].items()}
        for item in data:
            for key in item.keys():
                hold_dict[key].append(item[key])
        self.df = pd.DataFrame(hold_dict)



if __name__ == '__main__':
    store_list = init_stores(STORE_DICT)
    prod_collect = []
    for st in store_list:
        class2call = STORE_MAP.get(st.name)
        prod_info = class2call('milk', st)
        prod_info.start_collecting_data()
        prod_collect.extend(prod_info._items)

    df = SearchResult(prod_collect)
