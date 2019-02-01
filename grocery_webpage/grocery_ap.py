from flask import Flask, render_template, request
import datetime
import pandas as pd

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scraper'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data_handling'))

from scraper import *
from data_management import SearchResult, TransformDf2Html
from site_language import *
app = Flask(__name__)

# global definitions
nav_lang = {}
country_code = {}
sterm = ''
sort_type = 'price'
prod_collect = []
df = SearchResult(prod_collect)


@app.route('/', methods=['GET'])
def index():
    global nav_lang
    global country_code
    global error_lang
    global prod_collect
    country_code = request.args.get('country', 'UK')
    prod_collect = []   # if there was something in it, clear it
    return(render_template('index.html', lang=index_search_lang[country_code], nav_lang=navbar_lang[country_code], err_lang=error_lang[country_code]))

@app.route('/results', methods=['POST'])
def results():
    global nav_lang
    global country_code
    global error_lang
    global results_lang
    global sterm
    global sort_type
    global prod_collect
    global df

    sterm = request.form.get('term', sterm)
    stype = request.form.get('sort_type', sort_type)
    if sterm == '':
        return(render_template('error.html', err_lang=error_lang[country_code], nav_lang=navbar_lang[country_code]))
    store_list = init_stores(STORE_DICT[country_code])
    if prod_collect == []:
        for st in store_list:
            class2call = STORE_MAP[country_code].get(st.name)
            prod_info = class2call(sterm, st)
            prod_info.start_collecting_data()
            prod_collect.extend(prod_info._items)
        df = SearchResult(prod_collect)
        transdf = TransformDf2Html(df.df[['store_name', 'link', 'price', 'unit price', 'promotion']])
        html_return = transdf.df2html_table(id='myTable', table_class='table table-hover', header_class='thead-dark')
    else:
        # import pdb
        # pdb.set_trace()

        prod_collect = df.sort_df(byWhat=stype)


    return(render_template('results.html', sterm=prod_collect, nav_lang=navbar_lang[country_code], result_lan=results_lang[country_code]))

if __name__ == '__main__':
    app.run(debug = True)
