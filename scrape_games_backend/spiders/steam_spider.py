from bs4 import BeautifulSoup
import urllib.request

class SteamSpider(object):
    ''' Spider Class for http://store.steampowered.com/ site'''

    def __init__(self, domain = ''):
        self.start_urls = domain
        self.page = 1

    def get_next_page(self, soup):
        next_page_link = self.start_urls + '&page='+str(self.page)
        print (next_page_link)
        req = urllib.request.Request(next_page_link, headers={'User-Agent': 'Mozilla/5.0'})
        next_page = urllib.request.urlopen(req).read()
        next_page = BeautifulSoup(next_page, 'lxml')
        if 'pagebtn' in next_page.prettify():
            return next_page
        else:
            raise Exception



    def parse(self):

        req = urllib.request.Request(self.start_urls, headers = {'User-Agent' : 'Mozilla/5.0'})
        first_page = urllib.request.urlopen(req).read()

        soup_list = []
        soup_list.append(BeautifulSoup(first_page, 'lxml'))

        while True:
            try:

                new_soup = self.get_next_page(soup_list[-1])
                soup_list.append(new_soup)
                self.page += 1

            except:
                break


        for soup in soup_list:
            my_games = soup.select('a[data-ds-appid]')

            for game in my_games:

                deal = {}

                deal['title'] = game.find(class_ = 'title').text
                deal['link'] = game.get('href')
                deal['release_date'] = game.find(class_='col search_released responsive_secondrow').text
                try:
                    price = game.find(class_ = 'col search_price responsive_secondrow').text
                    deal['price'] = price.replace('\n', '').replace('\r', '').replace('\t', '')
                    deal['original_price'] = '/'
                    deal['discount'] = '/'
                except:
                    original_price = game.find(class_='col search_price discounted responsive_secondrow').strike.text
                    deal['original_price'] = original_price
                    price = game.find(class_='col search_price discounted responsive_secondrow').br.next_sibling
                    deal['price'] = price.replace('\t','')
                    deal['discount'] = game.find(class_='col search_discount responsive_secondrow').span.text

                yield deal


