from bs4 import BeautifulSoup
import re
import urllib.request

class GamersGateSpider(object):

    def __init__(self, domain=''):
        self.start_urls = domain
        self.soup_list = []

    def __str__(self):
        return 'Gamersgate'

    def get_next_page(self, soup):
        next_page_link = soup.find(class_="pgn_next")['href']
        next_page_link = 'http://www.gamersgate.com'+next_page_link
        next_page = urllib.request.urlopen(next_page_link).read()
        return BeautifulSoup(next_page.decode('utf-8'), 'lxml')

    def parse(self):

        first_page = urllib.request.urlopen(self.start_urls).read()
        first_page_data = BeautifulSoup(first_page.decode('utf-8'), 'lxml')

        self.soup_list.append(first_page_data)
        while len(self.soup_list) <= 2:
            try:
                soup = self.get_next_page(self.soup_list[-1])
                self.soup_list.append(soup)
            except:
                break

    def scrape(self):

        for soup in self.soup_list:
            list_of_games = soup.find(class_='biglist')
            my_games = []
            for game in list_of_games:
                my_games.append(game)

            for game in my_games:
                deal = {}

                platform_string = ''
                platforms = game.select('img[style*="vertical-align"]')
                platforms = [x['src'] for x in platforms]
                for plat in platforms:
                    if 'inline_pc' in plat:
                        platform_string += 'Win/'
                    elif 'inline_mac' in plat:
                        platform_string += 'Mac/'
                    elif 'inline_linux' in plat:
                        platform_string += 'Linux/'

                deal['platforms'] = platform_string[:-1]
                deal['store'] = 'GamersGate'
                deal['storelink'] = 'http://www.gamersgate.com/'
                deal['title'] = game.find(class_='ttl')['title']
                deal['link'] = game.find(class_='ttl')['href']
                deal['faketitle'] = re.sub(r'[^\w]', '', deal['title']).lower()

                price = game.find('span').text
                deal['price'] = float(price[:-2].replace(',', '.'))
                try:
                    original_price = game.find(class_='textstyle1').text
                    deal['original_price'] = float(original_price[:-2].replace(',', '.'))
                    deal['discount'] = game.find(class_='red bold bigger').text
                except:
                    deal['original_price'] = deal['price']

                yield deal