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

    def df2html_table(self, **kwargs):
        tid = kwargs.get('id', '')
        tclass = kwargs.get('table_class', '')
        hclass = kwargs.get('header_class', '')
        thead = self.create_table_header(hclass)
        tbody = self.create_table_body()
        html = '<table class="{cls}" id="{id}"> {thead} {tbody} </table>'.format(cls=tclass, id=tid, thead=thead, tbody=tbody)
        return html

    def create_table_header(self, hclass):
        cols = self.df.columns
        thb = ''
        for num, col in enumerate(cols):
            thb = thb + '<th onclick="sortTable({num})"> {text} </th>'.format(num=num, text=col.replace('_', ' ').capitalize())
        th = '<thead class="{hclass}"> <tr> {thead_body} </tr> </thead>'.format(hclass=hclass, thead_body=thb)
        return th

    def create_table_body(self):
        cols = self.df.columns
        tbb = ''
        for row in range(self.df.shape[0]):
            tbb = tbb + '<tr> '
            for col in cols:
                tbb = tbb + '<th> {text} </th>'.format(text=self.df.loc[row, col])
            tbb = tbb + '</tr>'
        tb = '<tbody> {body} </tbody>'.format(body=tbb)
        return tb




if __name__ == '__main__':
    store_list = init_stores(STORE_DICT)
    prod_collect = []
    for st in store_list:
        class2call = STORE_MAP.get(st.name)
        prod_info = class2call('alpro coconut', st)
        prod_info.start_collecting_data()
        prod_collect.extend(prod_info._items)

    df = SearchResult(prod_collect)
    html = df.df2html_table(id='myTable', table_class='table table-hover', header_class='thead-dark')
