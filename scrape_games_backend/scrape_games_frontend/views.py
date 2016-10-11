from django.shortcuts import redirect, render, reverse
from django.core.exceptions import ValidationError
from django.contrib import messages

from spiders.dl_gamer_spider import DlGamerSpider
from spiders.gmg_spider import GMGSpider

import os
import sys
import time


def home_page(request):

    messages.get_messages(request)

    return render(request, 'scrape_games_frontend/home.html')


def results_page(request):
    if request.method == 'GET':
        key = request.GET.get("q")


    print (key)
    linkWords = str(key).split()
    domain = ""
    for word in linkWords:
        domain += word + '+'
    domain = 'https://www.dlgamer.eu/advanced_search_result.php?keywords=' + domain[:-1]

    domain_gmg=""
    for word in linkWords:
        domain_gmg += word + '%20'
    domain_gmg = 'https://www.greenmangaming.com/search/' +domain_gmg[:-3]

    my_game = DlGamerSpider(domain)
    my_list = my_game.parse()

    gmg_game = GMGSpider(domain_gmg)
    gmg_list = gmg_game.parse()

    return render(request, 'scrape_games_frontend/results.html', {
                                                                      'my_list': my_list,
                                                                      'gmg_list': gmg_list,
                                                                      })
