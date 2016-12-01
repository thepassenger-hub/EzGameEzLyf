from bs4 import BeautifulSoup
import json
import re
import requests

class GMGSpider(object):
    ''' Spider Class for greenmangaming.com site'''
    def __init__(self, domain=''):
        self.start_urls = domain
        self.soup_list = []

    def __str__(self):
        return 'GreenManGaming'

    def get_next_page(self, soup):
        next_page_link = soup.find(rel='next')['href']
        next_page_url = 'https://www.greenmangaming.com' + next_page_link
        req = requests.get(next_page_url).content

        return BeautifulSoup(req, 'lxml')

    def parse(self):

        req = requests.get(self.start_urls).content

        self.soup_list.append(BeautifulSoup(req, 'lxml'))

        while len(self.soup_list) < 5:
            try:
                new_soup = self.get_next_page(self.soup_list[-1])

                print('nextpage')
                self.soup_list.append(new_soup)
            except:
                break

    def scrape(self):

        for soup in self.soup_list:

            deals = re.search('Products":(.+?),"ComingSoon"', soup.prettify()).group(1)
            my_games = json.loads(deals)

            for game in my_games:

                deal = {}

                deal['platforms'] = '/'
                deal['store'] = 'GreenManGaming'
                deal['storelink'] = 'https://www.greenmangaming.com/'
                deal['title'] = str(game['Name'])
                deal['faketitle'] = re.sub(r'[^\w]', '', deal['title']).lower()
                deal['link'] = deal['storelink'] + str(game['Url'])
                deal['original_price'] = float(game['DefaultVariant']['PreviousPrice'])
                deal['price'] = float(game['DefaultVariant']['CurrentPrice'])
                deal['release_date'] = str(game['DefaultVariant']['ReleasedDateText'])

                yield deal
