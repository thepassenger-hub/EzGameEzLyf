import requests
import json
import re

class GOGSpider(object):

    def __init__(self, domain=''):
        self.start_urls = domain
        self.data = None

    def __str__(self):
        return 'GOG'

    def parse(self):
        first_page = requests.get(self.start_urls).content
        self.data = json.loads(first_page.decode('utf-8'))

    def scrape(self):
        if self.data:
            for game in self.data['products']:

                deal = {}

                platform_string = ''
                platforms = game['worksOn']
                platforms = [x.replace('Windows','Win') for x in platforms if platforms[x] == True]
                platforms.sort(reverse=True)
                for plat in platforms:
                    platform_string += plat + '/'

                deal['platforms'] = platform_string[:-1]
                deal['store'] = 'GOG'
                deal['storelink'] = 'https://www.gog.com/'
                deal['title'] = game['title']
                deal['link'] = 'https://www.gog.com/game/'+game['slug']
                deal['faketitle'] = re.sub(r'[^\w]', '', deal['title']).lower()
                deal['price'] = float(game['price']['amount'])
                deal['original_price'] = float(game['price']['baseAmount'])
                deal['discount'] = game['price']['discountPercentage']
                if not deal['discount']:
                    deal['discount'] = '/'

                yield deal


