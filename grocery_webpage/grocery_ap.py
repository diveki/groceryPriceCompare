from flask import Flask, render_template, request
import datetime
import pandas as pd

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scraper'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data_handling'))

from scraper import *
from data_management import SearchResult

app = Flask(__name__)

@app.route('/')
def index():
    # return('Hello World')
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
    return(render_template('results.html', sterm=df.df.to_html()))
