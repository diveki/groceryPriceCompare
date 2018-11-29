'''
Scraping classes
'''

STORE_DICT = {'Tesco': {'url': 'https://www.tesco.com/groceries/en-GB/search?query=',
                        'page': 'page=',
                        'count': 'count='},
              'Sainsbury': {'url': 'https://www.sainsburys.co.uk/webapp/wcs/stores/servlet/SearchDisplayView?storeId=10151&searchTerm=',
                        'page': 'beginIndex=',
                        'count': 'pageSize='}
              }

class Store:
    pass


class Search:
    pass


def init_stores():
    pass


if __name__ == '__main__':
    init_stores()