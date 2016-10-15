from django.shortcuts import redirect, render, reverse
from django.core.exceptions import ValidationError
from django.contrib import messages

from spiders.run_spiders import run_spiders

import re



def home_page(request):

    messages.get_messages(request)

    return render(request, 'scrape_games_frontend/home.html')

def games_page(request):
    if request.method == 'GET':
        key = request.GET.get("q")
        if key.strip() == '':
            messages.add_message(request, messages.ERROR, "You must search something!")
            return redirect(home_page)

    games_list = run_spiders(key)
    title_list = []
    output_list = []

    for game_list in games_list:
        for game in game_list:
            fake_title = game['title']
            fake_title = re.sub(r'[^\w]', '', fake_title).lower()
            if fake_title not in title_list:
                title_list.append(fake_title)
                output_list.append(game)
            else:
                for prevgame in output_list:

                    try:
                        if re.sub(r'[^\w]', '', prevgame['title']).lower() == fake_title and\
                                        float(game['price']) < float(prevgame['price']):
                            print (str(game['price']) +'&&'+ str(prevgame['price']))
                            print ('RIMUOVO' + prevgame['title'])
                            output_list.remove(prevgame)
                            print ('AGGIUNGO' + game['title'])
                            output_list.append(game)
                    except:
                        pass
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
