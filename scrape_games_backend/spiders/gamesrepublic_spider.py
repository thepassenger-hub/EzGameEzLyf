import requests
from bs4 import BeautifulSoup
import re

class GamesRepublicSpider(object):

    def __init__(self, domain=''):
        self.start_urls = domain
        self.page_list = []

    def __str__(self):
        return 'GamesRepublic'

    def parse(self):
        first_page = requests.get(self.start_urls).content
        data = BeautifulSoup(first_page.decode('utf-8'), 'lxml')


        self.page_list.append(data)


    def scrape(self):
        for page in self.page_list:
            my_games = page.select('li')
            for game in my_games:

                deal = {}

                platform_string = ''
                platforms = game.select('i[class]')
                allowed = ['windows', 'mac', 'linux']
                for plat in platforms:
                    if plat['class'][0] in allowed:
                        platform_string += plat['class'][0].replace('windows', 'Win').capitalize() + '/'
                deal['platforms'] = platform_string[:-1]
                deal['store'] = 'GamesRepublic'
                deal['storelink'] = 'https://gamesrepublic.com/'
                deal['title'] = game.find('img')['alt']
                deal['link'] = 'https://gamesrepublic.com' + game.find('a')['href']
                deal['faketitle'] = re.sub(r'[^\w]', '', deal['title']).lower()
                deal['price'] = float(game.find(class_='price').text[1:].replace(',','.'))
                try:
                    deal['discount'] = game.select('span[class="promotion"]')[0].text
                    discount = float(deal['discount'][1:-1].replace(',','.'))/100
                    original_price = deal['price']/(1-discount)
                    deal['original_price'] = round(original_price,2)
                except:
                    deal['discount'] = '/'
                    deal['original_price'] = deal['price']

                yield deal