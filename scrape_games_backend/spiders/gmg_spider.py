from bs4 import BeautifulSoup
import json
import re
import urllib.request

class GMGSpider(object):
    ''' Spider Class for greenmangaming.com site'''
    def __init__(self, domain = ''):
        self.start_urls = domain

        self.soup_list = []

    def get_next_page(self, soup):
        next_page_link = soup.find(rel = 'next')['href']
        next_page_url = 'https://www.greenmangaming.com'+next_page_link

        req = urllib.request.Request(next_page_url, headers={'User-Agent': 'Mozilla/5.0'})
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

            deals = re.search('Products":(.+?),"ComingSoon"', soup.prettify()).group(1)



            my_games = json.loads(deals)
            for game in my_games:

                deal = {}

                deal['store'] = 'GreenManGaming'
                deal['storelink'] = 'https://www.greenmangaming.com/'
                deal['title'] = str(game['Name'])
                deal['faketitle'] = re.sub(r'[^\w]', '', deal['title']).lower()
                deal['link'] = deal['storelink']+str(game['Url'])
                deal['original_price'] = str(game['DefaultVariant']['PreviousPrice'])
                deal['price'] = float(game['DefaultVariant']['CurrentPrice'])
                deal['release_date'] = str(game['DefaultVariant']['ReleasedDateText'])

                yield deal
