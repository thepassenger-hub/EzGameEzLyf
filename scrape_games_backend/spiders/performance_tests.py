import gevent
from gevent.pool import Pool as gPool

from multiprocessing import Pool
from threading import Thread
from datetime import datetime

from urllib.parse import quote

from dl_gamer_spider import DlGamerSpider
from gmg_spider import GMGSpider
from gplanetuk_spider import GamesPlanetUKSpider
from steam_spider import SteamSpider
from gog_spider import GOGSpider
from humblebundle_api_spider import HumbleBundleApiSpider
from gamersgate_spider import GamersGateSpider
from indiegala_spider import IndieGalaSpider
from gplanetde_spider import GamesPlanetDESpider
from gplanetfr_spider import GamesPlanetFRSpider
from wingamestore_spider import WinGameStoreSpider

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

    domain_gplanetuk = 'https://uk.gamesplanet.com/search?utf8=%E2%9C%93&query=' + domain_gplanetuk[:-1]
    domain_gplanetde = 'https://de.gamesplanet.com/search?utf8=%E2%9C%93&query=' + domain_gplanetde[:-1]
    domain_gplanetfr = 'https://fr.gamesplanet.com/search?utf8=%E2%9C%93&query=' + domain_gplanetfr[:-1]
    domain_dlgamer = 'https://www.dlgamer.eu/advanced_search_result.php?keywords=' + domain_dlgamer[:-1]
    domain_gmg = 'https://www.greenmangaming.com/search/' + domain_gmg[:-3]
    domain_steam = 'http://store.steampowered.com/search/?term=' + domain_steam[:-3]
    domain_humblebundle = 'https://www.humblebundle.com/store/api?request=1&page_size=20&sort=bestselling&page=0&search=' + domain_humblebundle[:-1]
    domain_gog = 'https://www.gog.com/games/ajax/filtered?mediaType=game&page=1&sort=bestselling&search=' + domain_gog[:-1]
    domain_gamersgate = 'http://www.gamersgate.com/games?prio=relevance&q=' + domain_gamersgate[:-1]
    domain_indiegala = 'https://www.indiegala.com/store/search?type=games&key=' + domain_indiegala[:-3]
    domain_wingamestore = 'http://www.wingamestore.com/search/?SearchWord=' + domain_wingamestore[:-1]
    return domain_dlgamer, domain_gmg, domain_gplanetuk, domain_steam, \
           domain_humblebundle, domain_gog, domain_gamersgate, domain_indiegala, domain_gplanetde, domain_gplanetfr,\
           domain_wingamestore

def set_spiders(key):
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
    return [dlgamer_game, gmg_game, gplanetuk_game, steam_game, humblebundle_game, gamersgate_game,
            indiegala_game, gplanetde_game, gplanetfr_game, wingamestore_game], gog_game

class IpGetter(Thread):
    def __init__(self, spidername):
        Thread.__init__(self)
        self.spider = spidername
    def run(self):
        self.spider.parse()

def do_stuff(spider):

    spider.parse()
    return (list(spider.scrape()))

if __name__ == "__main__":
    keys = ['borderlands', 'rocket league', 'dark souls', 'grand theft auto']
    for key in keys:


        t1 = datetime.now()
        spiders, gog_game = set_spiders(key)
        pool = gPool(len(spiders))
        jobs = [pool.spawn(spider.parse()) for spider in spiders]
        pool.join()
        results = [list(spider.scrape()) for spider in spiders]
        results.append(list(gog_game.scrape()))
        t2 = datetime.now()
        print(results)
        print("Using gevent.Pool it took: %s" % (t2 - t1).total_seconds())
        print("-----------")
        t1 = datetime.now()
        spiders, gog_game = set_spiders(key)
        jobs = [gevent.spawn(spider.parse()) for spider in spiders]
        gevent.joinall(jobs, timeout=2)
        results = [list(spider.scrape()) for spider in spiders]
        results.append(list(gog_game.scrape()))
        print(results)
        t2 = datetime.now()
        print ("Using gevent it took: %s" % (t2-t1).total_seconds())
        print ("-----------")
        print("Starting to parse single files")
        t1 = datetime.now()
        spiders, gog_game = set_spiders(key)
        for spider in spiders:
            print("Now parsing: %s" % spider)
            spider.parse()
        results = [list(spider.scrape()) for spider in spiders]
        results.append(list(gog_game.scrape()))
        print(results)
        t2 = datetime.now()
        print ("It took: %s" % (t2-t1).total_seconds())
        t1 = datetime.now()
        spiders, gog_game = set_spiders(key)
        pool = Pool(len(spiders))
        test = pool.map(do_stuff, spiders)
        pool.close()
        pool.join()
        #results = [list(spider.scrape()) for spider in test]
        test.append(list(gog_game.scrape()))
        print(test)
        t2 = datetime.now()

        print ("Using multiprocessing it took: %s" % (t2-t1).total_seconds())
        print ("-----------")
        t1 = datetime.now()
        threads = []
        spiders, gog_game = set_spiders(key)
        for spider in spiders:
            t = IpGetter(spider)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        results = [list(spider.scrape()) for spider in spiders]
        results.append(list(gog_game.scrape()))
        print (results)

        t2 = datetime.now()
        print ("Using multi-threading it took: %s" % (t2-t1).total_seconds())