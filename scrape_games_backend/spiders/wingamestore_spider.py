from bs4 import BeautifulSoup
import requests
import re

CONVERT_RATE_URL = 'http://www.xe.com/currencyconverter/convert/?Amount=1&From=EUR&To=USD'
class WinGameStoreSpider(object):
    def __init__(self, domain=''):
        self.start_url = domain
        self.soup_list = []
        self.rate_coverter = 0.0

    def __str__(self):
        return 'WinGameStore'

    def parse(self):
        req_cur = requests.get(CONVERT_RATE_URL).content
        soup_cur = BeautifulSoup(req_cur, 'lxml')
        self.rate_coverter = float(soup_cur.find(class_='uccResultUnit')['data-amount'])

        page = requests.get(self.start_url)
        tup = BeautifulSoup(page.content.decode('utf-8'), 'lxml'), page.url

        self.soup_list.append(tup)

    def scrape(self):
        soup = self.soup_list[0][0]
        url = self.soup_list[0][1]
        if 'product' in url:
            deal = {}

            deal['store'] = 'WinGameStore'
            deal['platforms'] = 'Win'
            deal['storelink'] = 'http://www.wingamestore.com/'
            deal['title'] = soup.find(id="content-guts-title").text
            deal['faketitle'] = re.sub(r'[^\w]', '', deal['title']).lower()
            deal['link'] = url
            try:
                current_price = float(soup.find(class_='price').text[1:]) / self.rate_coverter
                deal['price'] = current_price
            except:
                deal['price'] = 0
            try:

                original_price = float(soup.find(class_='was').text[1:]) / self.rate_coverter
                deal['original_price'] = original_price
                a = soup.find(class_='onsale').text.split()
                discount = [y for y in a if '%' in y][0]
                deal['discount'] = discount

            except:
                deal['original_price'] = deal['price']
                deal['discount'] = '/'

            yield deal

        else:
            mygames = soup.select("tr[class*='result-row']")

            for game in mygames:
                deal = {}
                deal['store'] = 'WinGameStore'
                deal['platforms'] = 'Win'
                deal['storelink'] = 'http://www.wingamestore.com/'
                deal['title'] = game.find('a')['title']
                deal['faketitle'] = re.sub(r'[^\w]', '', deal['title']).lower()
                deal['link'] = deal['storelink'][:-1] + game.find('a')['href']
                try:
                    current_price = float(game.find(class_='price').text[1:]) / self.rate_coverter
                    deal['price'] = current_price
                except:
                    deal['price'] = 0
                try:
                    discount = game.find(class_='saletab').text.replace('SAVE','')[:-1]
                    deal['discount'] = '-'+discount+'%'
                    original_price = deal['price'] / ((100-float(discount))/100)
                    deal['original_price'] = original_price

                except:
                    deal['original_price'] = deal['price']
                    deal['discount'] = '/'

                yield deal





