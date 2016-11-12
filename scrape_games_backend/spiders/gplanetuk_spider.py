from bs4 import BeautifulSoup
import re
import urllib.request

CONVERT_RATE_URL = 'http://www.xe.com/currencyconverter/convert/?From=EUR&To=GBP'
class GamesPlanetUKSpider(object):
    ''' Spider Class for https://uk.gamesplanet.com site'''
    def __init__(self, domain=''):
        self.start_urls = domain
        self.soup_list = []
        self.rate_converter = 0.0

    def get_next_page(self, soup):
        next_page_link = soup.find(class_='next_page')['href']
        next_page_link = 'http://uk.gamesplanet.com' + next_page_link

        req = urllib.request.Request(next_page_link, headers={'User-Agent': 'Mozilla/5.0'})
        next_page = urllib.request.urlopen(req).read()
        return BeautifulSoup(next_page, 'lxml')

    def parse(self):
        req_cur = urllib.request.urlopen(CONVERT_RATE_URL).read()
        soup_cur = BeautifulSoup(req_cur, 'lxml')
        self.rate_coverter = float(soup_cur.find(class_='uccResultUnit')['data-amount'])

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

                platform_string = ''
                platforms = [plat['alt'].replace('Windows PC', 'Win').replace('Apple Mac', 'Mac') for
                             plat in game.select("img[class='platform_icon']")]
                for plat in platforms:
                    platform_string += plat + '/'

                deal['platforms'] = platform_string[:-1]
                deal['store'] = 'GamesPlanetUK'
                deal['storelink'] = 'https://uk.gamesplanet.com/'
                deal['title'] = game.find('a').text
                deal['faketitle'] = re.sub(r'[^\w]', '', deal['title']).lower()
                deal['link'] = deal['storelink'][:-1]+game.find('a')['href']
                try:
                    current_price = float(game.find(class_='price_current').text[1:]) / self.rate_coverter
                    current_price = '{:.2f}'.format(current_price)
                    deal['price'] = float(current_price)
                except:
                    deal['price'] = 0

                try:
                    original_price = float(game.find('strike').text[1:]) / self.rate_coverter
                    original_price = '{:.2f}'.format(original_price)
                    deal['original_price'] = original_price
                    deal['discount'] = game.find(class_='price_saving').text

                except:
                    deal['original_price'] = deal['price']
                    deal['discount'] = '/'

                deal['release_date'] = game.find('span').text


                yield deal
