from bs4 import BeautifulSoup
import re
import urllib.request

CONVERT_RATE_URL = 'http://www.xe.com/currencyconverter/convert/?From=EUR&To=GBP'
class GamesPlanetUKSpider(object):
    ''' Spider Class for https://uk.gamesplanet.com site'''
    def __init__(self, domain = ''):
        self.start_urls = domain
        self.soup_list = []
        req = urllib.request.urlopen('http://www.xe.com/currencyconverter/convert/?From=EUR&To=GBP').read()
        soup = BeautifulSoup(req, 'lxml')
        self.rate_coverter = float(soup.find(class_='uccResultUnit')['data-amount'])

    def get_next_page(self, soup):
        next_page_link = soup.find(class_='next_page')['href']
        next_page_link = 'http://uk.gamesplanet.com' + next_page_link

        req = urllib.request.Request(next_page_link, headers={'User-Agent': 'Mozilla/5.0'})
        next_page = urllib.request.urlopen(req).read()
        return BeautifulSoup(next_page, 'lxml')

    def parse(self):

        req = urllib.request.Request(self.start_urls, headers={'User-Agent': 'Mozilla/5.0'})
        first_page = urllib.request.urlopen(req).read()

        self.soup_list.append(BeautifulSoup(first_page, 'lxml'))

        while True:
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

                deal['store'] = 'GamesPlanetUK'
                deal['storelink'] = 'https://uk.gamesplanet.com/'
                deal['title'] = game.find('a').text
                deal['faketitle'] = re.sub(r'[^\w]', '', deal['title']).lower()
                deal['link'] = deal['storelink']+game.find('a')['href']
                try:
                    original_price = float(game.find('strike').text[1:]) / self.rate_coverter
                    original_price = '{:.2f}'.format(original_price)
                    deal['original_price'] = original_price
                except:
                    pass
                deal['release_date'] = game.find('span').text
                try:
                    original_price = float(game.find(class_='price_current').text[1:]) / self.rate_coverter
                    original_price = '{:.2f}'.format(original_price)
                    deal['price'] = float(original_price)
                except:
                    pass

                yield deal
