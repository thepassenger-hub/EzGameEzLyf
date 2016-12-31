from threading import Thread
import re
from urllib.parse import quote
from requests.exceptions import RequestException
# Importing the spiders

from .dl_gamer_spider import DlGamerSpider
from .gmg_spider import GMGSpider
from .gplanetuk_spider import GamesPlanetUKSpider
from .gplanetde_spider import GamesPlanetDESpider
from .gplanetfr_spider import GamesPlanetFRSpider
from .steam_spider import SteamSpider
from .gog_spider import GOGSpider
from .humblebundle_api_spider import HumbleBundleApiSpider
from .gamersgate_spider import GamersGateSpider
from .indiegala_spider import IndieGalaSpider
from .wingamestore_spider import WinGameStoreSpider
from .macgamestore_spider import MacGameStoreSpider
from .bundlestars_spider import BundleStarsApiSpider
from .direct2drive_spider import Direct2DriveApiSpider
from .gamesrepublic_spider import GamesRepublicSpider

def set_domains(key):
    domain_dlgamer = ''
    domain_gmg = ''
    domain_gplanetuk = ''
    linkWords = [ quote(word) for word in key.split()]
    print (linkWords)
    for word in linkWords:
        domain_dlgamer += word + '+'
        domain_gmg += word + '%20'
        domain_gplanetuk += word + '+'
    domain_steam = domain_gmg
    domain_humblebundle = domain_dlgamer
    domain_gog = domain_dlgamer
    domain_gamersgate = domain_dlgamer
    domain_indiegala = domain_gmg
    domain_gplanetde = domain_gplanetuk
    domain_gplanetfr = domain_gplanetde
    domain_wingamestore = domain_gplanetuk
    domain_macgamestore = domain_wingamestore
    domain_bundlestars = domain_gplanetuk
    domain_direct2drive = domain_gplanetuk
    domain_gamesrepublic = domain_gplanetuk

    domain_gplanetuk = 'https://uk.gamesplanet.com/search?utf8=%E2%9C%93&query=' + domain_gplanetuk[:-1]
    domain_gplanetde = 'https://de.gamesplanet.com/search?utf8=%E2%9C%93&query=' + domain_gplanetde[:-1]
    domain_gplanetfr = 'https://fr.gamesplanet.com/search?utf8=%E2%9C%93&query=' + domain_gplanetfr[:-1]
    domain_dlgamer = 'https://www.dlgamer.eu/advanced_search_result.php?keywords=' + domain_dlgamer[:-1]
    domain_gmg = 'https://www.greenmangaming.com/search/' + domain_gmg[:-3]+'?platform=73'
    domain_steam = 'http://store.steampowered.com/search/?term=' + domain_steam[:-3]
    domain_humblebundle = 'https://www.humblebundle.com/store/api?request=1&page_size=20&sort=bestselling&page=0&search=' + domain_humblebundle[:-1]
    domain_gog = 'https://www.gog.com/games/ajax/filtered?mediaType=game&page=1&sort=bestselling&search=' + domain_gog[:-1]
    domain_gamersgate = 'http://www.gamersgate.com/games?prio=relevance&q=' + domain_gamersgate[:-1]
    domain_indiegala = 'https://www.indiegala.com/store/search?type=games&key=' + domain_indiegala[:-3]
    domain_wingamestore = 'http://www.wingamestore.com/search/?SearchWord=' + domain_wingamestore[:-1]
    domain_macgamestore = 'http://www.macgamestore.com/search/?SearchWord=' + domain_macgamestore[:-1]
    domain_bundlestars = 'https://www.bundlestars.com/api/products?pageSize=50&search='+ domain_bundlestars[:-1]+'&'
    domain_direct2drive = 'https://www.direct2drive.com/backend/api/productquery/findpage?pagesize=100&search.keywords=' + domain_direct2drive[:-1]
    domain_gamesrepublic = 'https://gamesrepublic.com/catalog/getproductitems.html?page=0&itemsPerPage=50&productName=' + domain_gamesrepublic[:-1]

    return domain_dlgamer, domain_gmg, domain_gplanetuk, domain_steam, \
           domain_humblebundle, domain_gog, domain_gamersgate, domain_indiegala, domain_gplanetde, domain_gplanetfr,\
           domain_wingamestore, domain_macgamestore, domain_bundlestars, domain_direct2drive, domain_gamesrepublic

def is_sublist(input_key, title):
    for word in input_key:
        if word not in title:
            return False
    return True

def filter(key, game_list):

    """
    Filters the deals by looking at the deal title.
    If key of query is 'ashes ariandel' check into title words if there are both 'ashes' and 'ariandel'.
    Order doesnt matter.
    """

    filtered_list = []
    key_input = key.lower().split()
    for game in game_list:
        title = re.sub(r'[^\w]', ' ', game['title']).lower().split()
        if is_sublist(key_input, title):
            filtered_list.append(game)
    return filtered_list


class SpiderThread(Thread):

    """
    Launches every spider as a Thread.
    If the parsing phase is successful increments the progres bar by 100/(n spiders).
    If it returns error the spider gets added to an offline spiders array and it will be shown as error in the template.
    """

    def __init__(self, spidername):
        Thread.__init__(self)
        self.spider = spidername

    def run(self):
        try:
            self.spider.parse()
        except RequestException as e:
            print (e)
            offline.append(self.spider)


def set_spiders(key, excluded):

    domains = set_domains(key)

    dlgamer_game = DlGamerSpider(domains[0])
    gmg_game = GMGSpider(domains[1])
    gplanetuk_game = GamesPlanetUKSpider(domains[2])
    steam_game = SteamSpider(domains[3])
    humblebundle_game = HumbleBundleApiSpider(domains[4])
    gog_game = GOGSpider(domains[5])
    gamersgate_game = GamersGateSpider(domains[6])
    indiegala_game = IndieGalaSpider(domains[7])
    gplanetde_game = GamesPlanetDESpider(domains[8])
    gplanetfr_game = GamesPlanetFRSpider(domains[9])
    wingamestore_game = WinGameStoreSpider(domains[10])
    macgamestore_game = MacGameStoreSpider(domains[11])
    bundlestars_game = BundleStarsApiSpider(domains[12])
    direct2drive_game = Direct2DriveApiSpider(domains[13])
    gamesrepublic_game = GamesRepublicSpider(domains[14])
    spiders_filtered = [dlgamer_game, indiegala_game, wingamestore_game, macgamestore_game,]
    spiders_not_filtered = [gmg_game, gplanetuk_game, steam_game, humblebundle_game, gamersgate_game,
                            gplanetde_game, gplanetfr_game, bundlestars_game, direct2drive_game, gog_game]
    if excluded:
        spiders_filtered = [spider for spider in spiders_filtered if str(spider) not in excluded]
        spiders_not_filtered = [spider for spider in spiders_not_filtered if str(spider) not in excluded]

    return spiders_filtered, spiders_not_filtered


def run_spiders(key, excluded):

    global offline
    offline = []
    threads = []

    spiders_filtered, spiders_not_filtered = set_spiders(key, excluded)
    spiders = spiders_filtered + spiders_not_filtered
    for spider in spiders:
        t = SpiderThread(spider)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

    # progress.delete() # The progress bar is not needed anymore as it reached 100%
    results = []
    results_filtered = []
    for spider in spiders_not_filtered:
        if spider not in offline:
            try:
                results.append(list(filter(key, spider.scrape())))
            except Exception as e:
                print(e)
                offline.append(spider)
    for spider in spiders_filtered:
        if spider not in offline:
            try:
                results_filtered.append(list(filter(key, spider.scrape())))
            except Exception as e:
                print(e)
                offline.append(spider)
    # results = [list(filter(key,spider.scrape())) for spider in spiders_not_filtered]
    # results_filtered = [list(spider.scrape()) for spider in spiders_filtered]
    results += results_filtered
    return results, offline