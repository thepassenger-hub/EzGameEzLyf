from bs4 import BeautifulSoup
import dryscrape
import re
import sys


class HumbleBundleSpider(object):
    ''' Spider Class for https://www.humblebundle.com/store site'''

    def __init__(self, domain=''):
        if 'linux' in sys.platform:
            # start xvfb in case no X is running. Make sure xvfb
            # is installed, otherwise this won't work!
            dryscrape.start_xvfb()

        self.start_urls = domain
        self.soup_list = []
        self.session = dryscrape.Session()
        self.session.set_attribute('auto_load_images', False)

    def get_next_page(self, soup):
        next_page_buttons = soup.select('a[class="js-internal-store-link page-link"]')
        print (len(next_page_buttons))
        print (next_page_buttons[-1].text)
        if next_page_buttons[-1].text == 'Next':
            next_page_link = next_page_buttons[-1]['href']
        else:
            raise Exception
        next_page_link = 'https://www.humblebundle.com' + next_page_link
        self.session.visit(next_page_link)
        next_page = self.session.body()

        return BeautifulSoup(next_page, 'lxml')

    def parse(self):

        self.session.visit(self.start_urls)
        first_page = self.session.body()
        self.soup_list.append(BeautifulSoup(first_page, 'lxml'))

        while len(self.soup_list) <= 2:
            try:
                print ('tel chi')
                new_soup = self.get_next_page(self.soup_list[-1])
                self.soup_list.append(new_soup)
            except:
                break

    def scrape(self):

        for soup in self.soup_list:
            my_games = soup.select('div[data-product]')

            for game in my_games:

                deal = {}

                deal['platforms'] = []
                deal['store'] = 'HumbleBundle'
                deal['storelink'] = 'https://www.humblebundle.com/store'
                deal['link'] = game.find('a')['href']
                deal['title'] = game.find('h2').text
                deal['faketitle'] = re.sub(r'[^\w]', '', deal['title']).lower()
                price = game.find(class_='text store-price').text
                deal['price'] = float(price.replace('\n', '').replace(' ', '').replace(',','.')[1:])
                try:
                    deal['discount'] = game.find(class_='discount').text
                    percent = (float(deal['discount'][:-1])+100)/100
                    original_price = deal['price'] / percent
                    deal['original_price'] = '{:.2f}'.format(original_price)
                except:
                    pass

                yield deal

