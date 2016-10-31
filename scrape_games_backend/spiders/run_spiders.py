from gevent.pool import Pool
import re
from urllib.parse import quote

from .dl_gamer_spider import DlGamerSpider
from .gmg_spider import GMGSpider
from .gplanetuk_spider import GamesPlanetUKSpider
from .steam_spider import SteamSpider
from .gog_spider import GOGSpider
#from .humblebundle_spider import HumbleBundleSpider


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
    domain_humblebundle = domain_steam
    domain_gog = domain_dlgamer
    domain_gplanetuk = 'https://uk.gamesplanet.com/search?utf8=%E2%9C%93&query=' + domain_gplanetuk[:-1]
    domain_dlgamer = 'https://www.dlgamer.eu/advanced_search_result.php?keywords=' + domain_dlgamer[:-1]
    domain_gmg = 'https://www.greenmangaming.com/search/' + domain_gmg[:-3]
    domain_steam = 'http://store.steampowered.com/search/?term=' + domain_steam[:-3]
    domain_humblebundle = 'https://www.humblebundle.com/store/search/search/' + domain_humblebundle[:-3]
    domain_gog = 'https://www.gog.com/games/ajax/filtered?mediaType=game&page=1&sort=bestselling&search=' + domain_gog[:-1]

    return domain_dlgamer, domain_gmg, domain_gplanetuk, domain_steam, domain_humblebundle, domain_gog

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
    print (domains[5])
    dlgamer_game = DlGamerSpider(domains[0])
    gmg_game = GMGSpider(domains[1])
    gplanetuk_game = GamesPlanetUKSpider(domains[2])
    steam_game = SteamSpider(domains[3])
    #humblebundle_game = HumbleBundleSpider(domains[4])
    gog_game = GOGSpider(domains[5])

    pool = Pool(4)
    pool.spawn(dlgamer_game.parse())
    pool.spawn(gmg_game.parse())
    pool.spawn(gplanetuk_game.parse())
    pool.spawn(steam_game.parse())
    #pool.spawn(humblebundle_game.parse())
    pool.join()

    dlgamer_list = list(dlgamer_game.scrape())
    gmg_list = gmg_game.scrape()
    gmg_list_filtered = list(filter(key, gmg_list))
    gplanetuk_list = gplanetuk_game.scrape()
    gplanetuk_list_filtered = list(filter(key, gplanetuk_list))
    steam_list = steam_game.scrape()
    steam_list_filtered = list(filter(key, steam_list))
    print('quaqua')
    gog_list = list(gog_game.scrape())
    print('boh')
    #humblebundle_list = humblebundle_game.scrape()
    #humblebundle_list_filtered = list(filter(key, humblebundle_list))
    print(gog_list)

    return [dlgamer_list, gmg_list_filtered, gplanetuk_list_filtered, steam_list_filtered, gog_list]