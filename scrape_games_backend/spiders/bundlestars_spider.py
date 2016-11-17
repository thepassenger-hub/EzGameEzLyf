import urllib.request
import json
import re
from math import floor

class BundleStarsApiSpider(object):

    def __init__(self, domain=''):
        self.start_urls = domain
        self.page_list = []

    def get_next_pages(self):
        next_page_link = self.start_urls+'page=2'
        req = urllib.request.Request(next_page_link, headers={'User-Agent': 'Mozilla/5.0'})
        next_page = urllib.request.urlopen(req).read()
        next_page_data = json.loads(next_page.decode('utf-8'))

        return next_page_data




    def parse(self):
        req = urllib.request.Request(self.start_urls, headers={'User-Agent': 'Mozilla/5.0'})
        first_page = urllib.request.urlopen(req).read()
        data = json.loads(first_page.decode('utf-8'))


        self.page_list.append(data)

        if self.page_list[-1]['paging']['nextPage']:
            next_page_data = self.get_next_pages()
            self.page_list.append(next_page_data)

    def scrape(self):
        for page in self.page_list:

            for game in page['products']:

                deal = {}

                platform_string = ''
                platforms = [x.replace('windows','win') for x in game['_source']['platforms'] if game['_source']['platforms'][x]]
                platforms.sort(reverse=True)
                for plat in platforms:
                    platform_string += plat.capitalize()+'/'

                deal['platforms'] = platform_string[:-1]
                deal['store'] = 'BundleStars'
                deal['storelink'] = 'https://www.bundlestars.com/'
                deal['title'] = game['_source']['name']
                deal['link'] = 'https://www.bundlestars.com/game/' + game['_source']['slug']
                deal['faketitle'] = re.sub(r'[^\w]', '', deal['title']).lower()
                original_price_int = game['_source']['price']['EUR']
                original_price = float(str(original_price_int)[:-2] + '.' + str(original_price_int)[-2:])
                deal['original_price'] = original_price
                try:
                    discount = game['_source']['current_discount']['percent']
                except:
                    discount = 0

                if discount:
                    deal['discount'] = '-'+str(int(discount*100))+'%'
                    price = str(floor(original_price_int - original_price_int * discount))
                    price = float(price[:-2] + '.' + price[-2:])
                    deal['price'] = price
                else:
                    deal['discount'] = 0
                    deal['price'] = deal['original_price']

                yield deal