from bs4 import BeautifulSoup
import re
import urllib.request

class GamesPlanetDESpider(object):
    ''' Spider Class for https://fr.gamesplanet.com site'''
    def __init__(self, domain=''):
        self.start_urls = domain
        self.soup_list = []

    def get_next_page(self, soup):
        next_page_link = soup.find(class_='next_page')['href']
        next_page_link = 'http://de.gamesplanet.com' + next_page_link

        req = urllib.request.Request(next_page_link, headers={'User-Agent': 'Mozilla/5.0'})
        next_page = urllib.request.urlopen(req).read()
        return BeautifulSoup(next_page, 'lxml')

    def parse(self):

        req = urllib.request.Request(self.start_urls, headers={'User-Agent': 'Mozilla/5.0'})
        first_page = urllib.request.urlopen(req).read()

        self.soup_list.append(BeautifulSoup(first_page, 'lxml'))

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

                deal['store'] = 'GamesPlanetDE'
                deal['storelink'] = 'https://de.gamesplanet.com/'
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
