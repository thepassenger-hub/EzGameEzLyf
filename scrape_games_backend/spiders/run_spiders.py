'''from gevent import monkey
monkey.patch_all()'''
from gevent.pool import Pool

from .dl_gamer_spider import DlGamerSpider
from .gmg_spider import GMGSpider
from .gplanetuk_spider import GamesPlanetUKSpider
from .steam_spider import SteamSpider


def set_domains(key):
    domain_steam = ''
    domain_dlgamer = ''
    domain_gmg = ''
    domain_gplanetuk = ''
    linkWords = str(key).split()
    for word in linkWords:
        domain_dlgamer += word + '+'
        domain_gmg += word + '%20'
        domain_gplanetuk += word + '+'
    domain_steam = domain_gmg
    domain_gplanetuk = 'https://uk.gamesplanet.com/search?utf8=%E2%9C%93&query=' + domain_gplanetuk[:-1]
    domain_dlgamer = 'https://www.dlgamer.eu/advanced_search_result.php?keywords=' + domain_dlgamer[:-1]
    domain_gmg = 'https://www.greenmangaming.com/search/' + domain_gmg[:-3]
    domain_steam = 'http://store.steampowered.com/search/?term=' + domain_steam[:-3]

    return domain_dlgamer, domain_gmg, domain_gplanetuk, domain_steam

def run_spiders(key):
    pool = Pool(10)
    domains = set_domains(key)
    dlgamer_game = DlGamerSpider(domains[0])
    gmg_game = GMGSpider(domains[1])
    gplanetuk_game = GamesPlanetUKSpider(domains[2])
    steam_game = SteamSpider(domains[3])
    pool.spawn(run=dlgamer_game.parse())
    pool.spawn(run=gmg_game.parse())
    pool.spawn(run=gplanetuk_game.parse())
    pool.spawn(run=steam_game.parse())
    pool.join()
    return  dlgamer_game.scrape(), gmg_game.scrape(), gplanetuk_game.scrape(), steam_game.scrape()