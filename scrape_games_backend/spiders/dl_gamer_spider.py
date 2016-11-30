from bs4 import BeautifulSoup
import re
import requests

class DlGamerSpider(object):
    ''' Spider Class for dlgamer.eu site'''
    def __init__(self, domain=''):
        self.start_urls = domain
        self.soup_list = []

    def __str__(self):
        return 'DlGamer'

    def get_next_page(self, soup):
        next_page_link = soup.find(class_ ='nextpage')['href']
        next_page = requests.get(next_page_link).content
        return BeautifulSoup(next_page, 'lxml')

    def parse(self):
        first_page = requests.get(self.start_urls).content
        self.soup_list.append(BeautifulSoup(first_page, 'lxml'))

        while True:
            try:
                new_soup = self.get_next_page(self.soup_list[-1])
                self.soup_list.append(new_soup)
            except:
                break

    def scrape(self):

        for soup in self.soup_list:
            my_games = soup.select('div[class="mea_bloc_dart product"]')
            for game in my_games:

                deal = {}

                deal['title'] = game.find(class_='mea_bloc_dart_link').text
                platform_string = ''
                platforms = game.select('img')
                platforms = [x['src'] for x in platforms[1:]]

                for plat in platforms:
                    if 'windows' in plat:
                        platform_string += 'Win/'
                    elif 'mac' in plat:
                        platform_string += 'Mac/'
                if 'Linux' in deal['title']:
                    platform_string += 'Linux/'
                deal['platforms'] = platform_string[:-1]
                deal['store'] = 'DlGamer'
                deal['storelink'] = 'http://www.dlgamer.eu/'

                deal['faketitle'] = re.sub(r'[^\w]', '', deal['title']).lower()
                deal['link'] = game.find(class_ = 'mea_bloc_dart_link')['href']
                deal['original_price'] = game.find(class_ = 'mea_bloc_dart_price_strike product_price_strike').text[:-1]
                deal['price'] = float(game.find(class_ = 'mea_bloc_dart_price product_price').text[:-1])
                deal['discount'] = game.find(class_ = 'mea_bloc_dart_purcent product_purcent').text

                yield deal