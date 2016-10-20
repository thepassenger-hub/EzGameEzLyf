from django.shortcuts import redirect, render, reverse
from django.contrib import messages

from spiders.run_spiders import run_spiders

import re


def run_scrapers(key):
    spider_list = run_spiders(key)
    return spider_list

def filter_list(store_query_list, key):

    title_list = []
    output_list = []

    for game_list in store_query_list:
        for game in game_list:
            fake_title = game['title']
            fake_title = re.sub(r'[^\w]', '', fake_title).lower()
            if fake_title not in title_list:
                title_list.append(fake_title)
                game['faketitle'] = fake_title
                output_list.append(game)
            else:
                for prevgame in output_list:
                    try:
                        if re.sub(r'[^\w]', '', prevgame['title']).lower() == fake_title and \
                                            game['price'] < prevgame['price']:
                            print(str(game['price']) + '&&' + str(prevgame['price']))
                            print('RIMUOVO' + prevgame['title'])
                            output_list.remove(prevgame)
                            print('AGGIUNGO' + game['title'])
                            game['faketitle'] = fake_title
                            output_list.append(game)
                    except:
                        pass
    return output_list

def home_page(request):

    messages.get_messages(request)
    return render(request, 'scrape_games_frontend/home.html')

def selected_game(request):
    store_query_list = request.session['store_query_list']
    list_of_games = []
    title = request.GET.get("id")

    for game_list in store_query_list:
        for game in game_list:
            fake_title = game['title']
            fake_title = re.sub(r'[^\w]', '', fake_title).lower() #Removes non alphabetical characters and spaces
                                                                  #Grand Theft Auto III (Mac) -> grandtheftautoiiimac
            if fake_title == title:
                list_of_games.append(game)


    list_of_games = sorted(list_of_games, key=lambda k: k['price'])

    return render(request, 'scrape_games_frontend/single_deals.html', {
                                                                        'list_of_games': list_of_games,
                                                                       })


def games_page(request):

    if request.method == 'GET':
        key = request.GET.get("q")
        print (key)
        if key.strip() == '':
            messages.add_message(request, messages.ERROR, "You must search something!")
            return redirect(home_page)

    store_query_list = run_scrapers(key)
    request.session['store_query_list'] = store_query_list

    output_list = filter_list(store_query_list, key)
    output_list = sorted(output_list, key=lambda k: k['title'])

    return render(request, 'scrape_games_frontend/games_page.html', {
                                                                        'output_list': output_list,
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
