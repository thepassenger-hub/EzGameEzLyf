from bs4 import BeautifulSoup
import urllib.request
import re

CONVERT_RATE_URL = 'http://www.xe.com/currencyconverter/convert/?Amount=1&From=EUR&To=USD'
class MacGameStoreSpider(object):
    def __init__(self, domain=''):
        self.start_url = domain
        self.soup_list = []
        self.rate_coverter = 0.0

    def parse(self):
        req_cur = urllib.request.urlopen(CONVERT_RATE_URL).read()
        soup_cur = BeautifulSoup(req_cur, 'lxml')
        self.rate_coverter = float(soup_cur.find(class_='uccResultUnit')['data-amount'])

        page = urllib.request.urlopen(self.start_url).read()
        self.soup_list.append(BeautifulSoup(page.decode('utf-8'), 'lxml'))

    def scrape(self):
        for soup in self.soup_list:
            mygames = soup.select("tr[class*='result-row']")

            for game in mygames:
                deal = {}
                deal['store'] = 'MacGameStore'
                deal['platforms'] = ['Mac']
                deal['storelink'] = 'http://www.macgamestore.com/'
                deal['title'] = game.find('a')['title']
                deal['faketitle'] = re.sub(r'[^\w]', '', deal['title']).lower()
                deal['link'] = deal['storelink'][:-1] + game.find('a')['href']
                try:
                    current_price = float(game.find(class_='price').text[1:]) / self.rate_coverter
                    current_price = '{:.2f}'.format(current_price)
                    deal['price'] = float(current_price)
                except:
                    deal['price'] = 0
                try:
                    discount = game.find(class_='saletab').text.replace('SAVE','')[:-1]
                    deal['discount'] = '-'+discount+'%'
                    original_price = '{:.2f}'.format(deal['price'] / ((100-float(discount))/100))
                    deal['original_price'] = original_price

                except:
                    deal['original_price'] = deal['price']
                    deal['discount'] = '/'

                yield deal

