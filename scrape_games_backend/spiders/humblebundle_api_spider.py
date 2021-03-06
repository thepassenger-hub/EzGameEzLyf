import requests
import json
import re

class HumbleBundleApiSpider(object):

    def __init__(self, domain=''):
        self.start_urls = domain
        self.page_list = []

    def __str__(self):
        return 'HumbleBundle'

    def get_next_pages(self, page_number):
        next_page_link = re.sub(r'page=[0-9]', 'page=' + str(page_number), self.start_urls)
        next_page = requests.get(next_page_link).content
        next_page_data = json.loads(next_page.decode('utf-8'))

        if next_page_data['results']:
            return next_page_data['results']

        else:
            raise Exception



    def parse(self):
        first_page = requests.get(self.start_urls).content
        data = json.loads(first_page.decode('utf-8'))


        self.page_list.append(data['results'])

        while len(self.page_list) <= 2:
            try:
                next_page_data = self.get_next_pages(len(self.page_list))
                self.page_list.append(next_page_data)
            except:
                break

    def scrape(self):
        for page in self.page_list:

            for game in page:

                deal = {}

                platform_string = ''
                platforms = game['platforms']
                for plat in platforms:
                    platform_string += plat.replace('windows','Win').capitalize()+'/'

                deal['platforms'] = platform_string[:-1]
                deal['store'] = 'HumbleBundle'
                deal['storelink'] = 'https://www.humblebundle.com/store'
                deal['title'] = game['human_name']
                deal['link'] = 'https://www.humblebundle.com/store/' + game['human_url']
                deal['faketitle'] = re.sub(r'[^\w]', '', deal['title']).lower()
                try:
                    deal['price'] = game['current_price'][0]
                except:
                    deal['price'] = 0
                try:
                    deal['original_price'] = game['full_price'][0]
                except:
                    deal['original_price'] = 0
                if deal['original_price']:
                    deal['discount'] = '-'+str(round(100 * (deal['original_price'] - deal['price']) / deal['original_price']))+'%'
                else:
                    deal['discount'] = '/'
                yield deal