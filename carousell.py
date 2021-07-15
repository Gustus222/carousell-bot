from bs4 import BeautifulSoup as BS
import requests
import re


class CarousellScraper(object):
    def __init__(self, item):
        self.headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'}
        modified_item = re.sub(' ', '%20', item)
        self.source = requests.get(f'https://www.carousell.sg/search/{modified_item}?canChangeKeyword=false&sort_by=time_created%2Cdescending', headers=self.headers).text

    def get_page(self):
        return BS(self.source, 'lxml')
