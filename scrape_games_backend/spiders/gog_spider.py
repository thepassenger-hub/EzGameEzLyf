from urllib.request import urlopen
import json
import re

class GOGSpider(object):
    def __init__(self, domain=''):
        self.start_urls = domain

    def scrape(self):
        first_page = urlopen(self.start_urls).read()

        data = json.loads(first_page.decode('utf-8'))
        for game in data['products']:
            deal = {}
            deal['store'] = 'GOG'
            deal['storelink'] = 'https://www.gog.com/'
            deal['title'] = game['title']
            deal['link'] = 'https://www.gog.com/game/'+game['slug']
            deal['faketitle'] = re.sub(r'[^\w]', '', deal['title']).lower()
            deal['price'] = float(game['price']['amount'])
            deal['original_price'] = float(game['price']['baseAmount'])
            deal['discount'] = game['price']['discountPercentage']
            yield deal


