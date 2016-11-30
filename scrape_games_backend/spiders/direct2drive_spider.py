import requests
import json
import re


class Direct2DriveApiSpider(object):

    def __init__(self, domain=''):
        self.start_urls = domain
        self.page_list = []

    def __str__(self):
        return 'Direct2Drive'

    def parse(self):
        req = requests.get(self.start_urls).content
        data = json.loads(req.decode('utf-8'))

        self.page_list.append(data)


    def scrape(self):
        for page in self.page_list:
            for game in page['products']['items']:

                deal = {}

                platform_string = ''
                platforms = [str(x).replace('1100','Win').replace('1200','Mac') for x in game['platformIds']]

                for plat in platforms:
                    platform_string += plat+'/'

                deal['platforms'] = platform_string[:-1]
                deal['store'] = 'Direct2Drive'
                deal['storelink'] = 'https://www.direct2drive.com/'
                deal['title'] = game['title']
                deal['link'] = 'https://www.direct2drive.com/#!/download-' + game['uriSafeTitle']+'/'+str(game['id'])
                deal['faketitle'] = re.sub(r'[^\w]', '', deal['title']).lower()
                deal['price'] = float('{:.2f}'.format(float(game['offerActions'][0]['purchasePrice']['amount'])))
                deal['discount'] = '-'+str(round(float(game['offerActions'][0]['totalPercentOff']), 2))+'%'
                deal['original_price'] = float('{:.2f}'.format(float(game['offerActions'][0]['suggestedPrice']['amount'])))

                yield deal

if __name__ == '__main__':
    x = Direct2DriveApiSpider('https://www.direct2drive.com/backend/api/productquery/findpage?pagesize=100&search.keywords=darksiders')
    x.parse()
    print([y for y in x.scrape()])