from django.shortcuts import redirect, render, reverse
from django.contrib import messages

import re

from spiders.run_spiders import run_spiders


def run_scrapers(key):
    spider_list = run_spiders(key)
    return spider_list

def filter_list(store_query_list, key):

    title_list = []
    output_list = []

    for game_list in store_query_list:
        for game in game_list:
            fake_title = game['faketitle']
            if fake_title not in title_list:
                title_list.append(fake_title)
                output_list.append(game)
            else:
                for prevgame in output_list:

                    if prevgame['faketitle'] == fake_title and \
                                        game['price'] < prevgame['price']:
                        output_list.remove(prevgame)
                        output_list.append(game)


    return output_list

def home_page(request):

    messages.get_messages(request)
    return render(request, 'scrape_games_frontend/home.html')

def games_page(request):

    if request.method == 'GET':
        key = request.GET.get("q")
        if re.sub(r'[^\w]', '', key) == '':
            messages.add_message(request, messages.ERROR, "Invalid Input!")
            return redirect(home_page)

    store_query_list = run_scrapers(key)
    request.session['store_query_list'] = store_query_list

    output_list = filter_list(store_query_list, key)
    output_list = sorted(output_list, key=lambda k: k['title'])

    return render(request, 'scrape_games_frontend/games_page.html', {
                                                                        'output_list': output_list,
                                                                    })

def selected_game(request):
    store_query_list = request.session['store_query_list']
    list_of_games = []
    title = request.GET.get("id")

    for game_list in store_query_list:
        for game in game_list:
            fake_title = game['faketitle']
            if fake_title == title:
                list_of_games.append(game)


    list_of_games = sorted(list_of_games, key=lambda k: k['price'])

    return render(request, 'scrape_games_frontend/single_deals.html', {
                                                                        'list_of_games': list_of_games,
                                                                       })


def results_page(request):
    if request.method == 'GET':
        key = request.GET.get("q")
        if key.strip() == '':
            messages.add_message(request, messages.ERROR, "You must search something!")
            return redirect(home_page)

    dlgamer_list, gmg_list, gplanetuk_list, steam_list = run_spiders(key)

    return render(request, 'scrape_games_frontend/results.html', {
                                                                      'dlgamer_list': dlgamer_list,
                                                                      'gmg_list': gmg_list,
                                                                      'gplanetuk_list': gplanetuk_list,
                                                                      'steam_list': steam_list,
                                                                      })
