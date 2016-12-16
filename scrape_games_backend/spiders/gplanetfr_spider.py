from bs4 import BeautifulSoup
import re
import requests

class GamesPlanetFRSpider(object):
    ''' Spider Class for https://fr.gamesplanet.com site'''
    def __init__(self, domain=''):
        self.start_urls = domain
        self.soup_list = []

    def __str__(self):
        return 'GamesPlanetFR'

    def get_next_page(self, soup):
        next_page_link = soup.find(class_='next_page')['href']
        next_page_link = 'http://fr.gamesplanet.com' + next_page_link

        req = requests.get(next_page_link).content

        return BeautifulSoup(req, 'lxml')

    def parse(self):

        req = requests.get(self.start_urls).content

        self.soup_list.append(BeautifulSoup(req, 'lxml'))

        while len(self.start_urls) < 3:
            try:
                new_soup = self.get_next_page(self.soup_list[-1])
                self.soup_list.append(new_soup)
            except:
                break

    def scrape(self):

        for soup in self.soup_list:

            mygames = soup.select('div[class="details"]')
            for game in mygames:

                deal = {}

                platform_string = ''
                platforms = [plat['alt'].replace('Windows PC', 'Win').replace('Apple Mac', 'Mac') for
                             plat in game.select("img[class='platform_icon']")]
                for plat in platforms:
                    platform_string += plat + '/'

                deal['platforms'] = platform_string[:-1]
                deal['store'] = 'GamesPlanetFR'
                deal['storelink'] = 'https://fr.gamesplanet.com/'
                deal['title'] = game.find('a').text
                deal['faketitle'] = re.sub(r'[^\w]', '', deal['title']).lower()
                deal['link'] = deal['storelink'][:-1]+game.find('a')['href']
                try:
                    original_price = float(game.find('strike').text[:-1].replace(',','.'))
                    deal['original_price'] = original_price
                    deal['discount'] = game.find(class_='price_saving').text
                except:
                    pass
                deal['release_date'] = game.find('span').text
                try:
                    current_price = float(game.find(class_='price_current').text[:-1].replace(',','.'))
                    deal['price'] = current_price
                except:
                    deal['price'] = 0

                yield deal
