from gevent.pool import Pool
import re
from urllib.parse import quote

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
    #Filters the deals by looking at the deal title
    #if key of query is 'ashes ariandel' check into title words if there are both 'ashes' and 'ariandel'
    #order doesnt matter

    filtered_list = []
    key_input = key.lower().split()
    for game in game_list:
        title = re.sub(r'[^\w]', ' ', game['title']).lower().split()
        if is_sublist(key_input, title):
            filtered_list.append(game)
    return filtered_list


def run_spiders(key):

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

    pool = Pool(15)
    pool.spawn(dlgamer_game.parse())
    pool.spawn(gmg_game.parse())
    pool.spawn(gplanetuk_game.parse())
    pool.spawn(steam_game.parse())
    pool.spawn(humblebundle_game.parse())
    pool.spawn(gamersgate_game.parse())
    pool.spawn(indiegala_game.parse())
    pool.spawn(gplanetde_game.parse())
    pool.spawn(gplanetfr_game.parse())
    pool.spawn(wingamestore_game.parse())
    pool.spawn(macgamestore_game.parse())
    pool.spawn(bundlestars_game.parse())
    pool.spawn(direct2drive_game.parse())
    pool.spawn(gamesrepublic_game.parse())
    pool.spawn(gog_game.parse())
    pool.join()

    dlgamer_list = list(dlgamer_game.scrape())
    gmg_list = gmg_game.scrape()
    gmg_list_filtered = list(filter(key, gmg_list))
    gplanetuk_list = gplanetuk_game.scrape()
    gplanetuk_list_filtered = list(filter(key, gplanetuk_list))
    steam_list = steam_game.scrape()
    steam_list_filtered = list(filter(key, steam_list))
    gog_list = gog_game.scrape()
    gog_list_filtered = list(filter(key, gog_list))
    humblebundle_list = humblebundle_game.scrape()
    humblebundle_list_filtered = list(filter(key, humblebundle_list))
    gamersgate_list = gamersgate_game.scrape()
    gamersgate_list_filtered = list(filter(key, gamersgate_list))
    indiegala_list = list(indiegala_game.scrape())
    gplanetde_list = gplanetde_game.scrape()
    gplanetde_list_filtered = list(filter(key, gplanetde_list))
    gplanetfr_list = gplanetfr_game.scrape()
    gplanetfr_list_filtered = list(filter(key, gplanetfr_list))
    wingamestore_list = list(wingamestore_game.scrape())
    macgamestore_list = list(macgamestore_game.scrape())
    bundlestars_list = bundlestars_game.scrape()
    bundlestars_list_filtered = list(filter(key, bundlestars_list))
    direct2drive_list = direct2drive_game.scrape()
    direct2drive_list_filtered = list(filter(key, direct2drive_list))
    gamesrepublic_list = list(gamesrepublic_game.scrape())
    return [dlgamer_list, gmg_list_filtered, gplanetuk_list_filtered,
            steam_list_filtered, humblebundle_list_filtered, gog_list_filtered,
            gamersgate_list_filtered, indiegala_list, gplanetde_list_filtered, gplanetfr_list_filtered, wingamestore_list,
            macgamestore_list, bundlestars_list_filtered, direct2drive_list_filtered, gamesrepublic_list]