from bs4 import BeautifulSoup
import re
import requests


class SteamSpider(object):
    ''' Spider Class for http://store.steampowered.com/ site'''

    def __init__(self, domain = ''):
        self.start_urls = domain
        self.soup_list = []

    def __str__(self):
        return 'Steam'

    def get_next_page(self, soup):
        my_list = soup.findAll(class_='pagebtn')
        for page in my_list:
            if page.text == '>':
                next_page_link = page['href']
                req = requests.get(next_page_link).content

                return BeautifulSoup(req, 'lxml')
        raise Exception

    def parse(self):

        req = requests.get(self.start_urls).content

        self.soup_list.append(BeautifulSoup(req, 'lxml'))

        while len(self.soup_list) <= 2:
            try:
                new_soup = self.get_next_page(self.soup_list[-1])
                self.soup_list.append(new_soup)
            except:
                break

    def scrape(self):

        for soup in self.soup_list:

            my_games = soup.select('a[data-ds-appid]')
            for game in my_games:

                deal = {}

                deal['store'] = 'Steam'
                platforms = game.select("span[class*='platform_img']")
                ban = ['steamplay', 'hmd_separator', 'htcvive', 'oculusrift']
                platforms = (str(x['class'][1]) for x in platforms if str(x['class'][1]) not in ban)
                out = ''
                for plat in platforms:
                    out += plat.capitalize()+'/'
                deal['platforms'] = out[:-1]
                deal['storelink'] = 'https://store.steampowered.com'
                deal['title'] = game.find(class_ ='title').text
                deal['faketitle'] = re.sub(r'[^\w]', '', deal['title']).lower()
                deal['link'] = game.get('href')
                deal['release_date'] = game.find(class_='col search_released responsive_secondrow').text
                try:
                    price = game.find(class_ = 'col search_price responsive_secondrow').text
                    deal['price'] = price.replace('\n', '').replace('\r', '').replace('\t', '').replace(',','.')[:-1]
                    deal['original_price'] = '/'
                    deal['discount'] = '/'
                except:
                    original_price = game.find(class_='col search_price discounted responsive_secondrow').strike.text
                    deal['original_price'] = original_price.replace(',','.')[:-1]
                    price = game.find(class_='col search_price discounted responsive_secondrow').br.next_sibling
                    deal['price'] = price.replace('\t','').replace(',','.')[:-1]
                    deal['discount'] = game.find(class_='col search_discount responsive_secondrow').span.text
                try:
                    deal['price'] = float(deal['price'])
                except ValueError:
                    deal['price'] = 0
                yield deal