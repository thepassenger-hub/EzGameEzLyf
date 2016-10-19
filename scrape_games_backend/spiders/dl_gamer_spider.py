from bs4 import BeautifulSoup
import urllib.request

class DlGamerSpider(object):
    ''' Spider Class for dlgamer.eu site'''
    def __init__(self, domain = ''):
        self.start_urls = domain
        self.soup_list = []

    def get_next_page(self, soup):
        next_page_link = soup.find(class_ = 'nextpage')['href']
        next_page = urllib.request.urlopen(next_page_link).read()
        return BeautifulSoup(next_page, 'lxml')

    def parse(self):
        first_page = urllib.request.urlopen(self.start_urls).read()

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

                deal['store'] = 'DlGamer'
                deal['storelink'] = 'http://www.dlgamer.eu/'
                deal['title'] = game.find(class_ = 'mea_bloc_dart_link').text
                deal['link'] = game.find(class_ = 'mea_bloc_dart_link')['href']
                deal['original_price'] = game.find(class_ = 'mea_bloc_dart_price_strike product_price_strike').text[:-1]
                deal['price'] = float(game.find(class_ = 'mea_bloc_dart_price product_price').text[:-1])
                deal['discount'] = game.find(class_ = 'mea_bloc_dart_purcent product_purcent').text

                yield deal
