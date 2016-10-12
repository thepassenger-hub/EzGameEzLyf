from django.shortcuts import redirect, render, reverse
from django.core.exceptions import ValidationError
from django.contrib import messages

from spiders.run_spiders import run_spiders




def home_page(request):

    messages.get_messages(request)

    return render(request, 'scrape_games_frontend/home.html')

def results_page(request):
    if request.method == 'GET':
        key = request.GET.get("q")

    dlgamer_list, gmg_list, gplanetuk_list, steam_list = run_spiders(key)


    return render(request, 'scrape_games_frontend/results.html', {
                                                                      'dlgamer_list': dlgamer_list,
                                                                      'gmg_list': gmg_list,
                                                                      'gplanetuk_list': gplanetuk_list,
                                                                      'steam_list': steam_list,
                                                                      })
