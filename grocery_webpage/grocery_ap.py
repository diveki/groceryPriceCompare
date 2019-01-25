from flask import Flask, render_template, request
import datetime
import pandas as pd

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scraper'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data_handling'))

from scraper import *
from data_management import SearchResult, TransformDf2Html

app = Flask(__name__)

@app.route('/')
def index():
    return(render_template('index.html'))

@app.route('/results', methods=['POST'])
def results():
    sterm = request.form.get('term')
    store_list = init_stores(STORE_DICT)
    prod_collect = []
    for st in store_list:
        class2call = STORE_MAP.get(st.name)
        prod_info = class2call(sterm, st)
        prod_info.start_collecting_data()
        prod_collect.extend(prod_info._items)
    df = SearchResult(prod_collect)
    transdf = TransformDf2Html(df.df[['store_name', 'link', 'price', 'unit price', 'promotion']])
    html_return = transdf.df2html_table(id='myTable', table_class='table table-hover', header_class='thead-dark')
    # return(render_template('results.html', sterm=html_return))
    return(render_template('results.html', sterm=prod_collect))

if __name__ == '__main__':
    app.run(debug = True)
