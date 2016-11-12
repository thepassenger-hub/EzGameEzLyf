from bs4 import BeautifulSoup
import urllib.request
import re

class IndieGalaSpider(object):
    def __init__(self, domain=''):
        self.start_urls = domain
        self.soup_list = []

    def parse(self):
        first_page = urllib.request.urlopen(self.start_urls).read()
        first_soup = BeautifulSoup(first_page.decode('utf-8'), 'lxml')
        self.soup_list.append(first_soup)

    def scrape(self):
        for soup in self.soup_list:
            my_games = soup.select("div[class*='game-row']")

            for game in my_games:

                deal = {}
                deal['platforms'] = []
                deal['store'] = 'Indiegala'
                platforms = ''
                platform_links = game.select("img[src*='/store-img/']")
                for plat in platform_links:
                    if 'windows-icon' in str(plat):
                        platforms += 'Win/'
                    elif 'apple-icon' in str(plat):
                        platforms += 'Mac/'
                    elif 'linux-icon' in str(plat):
                        platforms += 'Linux/'
                deal['platforms'] = platforms[:-1]
                deal['storelink'] = 'https://www.indiegala.com/store'
                deal['title'] = game.find('a')['title']
                deal['link'] = 'https://www.indiegala.com' + game.find('a')['href']
                deal['faketitle'] = re.sub(r'[^\w]', '', deal['title']).lower()
                try:
                    deal['original_price'] = float(game.find(class_='top').text[1:])
                    deal['price'] = float(game.find(class_='bottom').text[1:])
                    deal['discount'] = game.find(class_='prices-cont').find(class_='left').text

                except:
                    deal['price'] = float(game.find(class_='price-cont').text[1:])
                    deal['original_price'] = deal['price']
                    deal['discount'] = 0

                yield deal


