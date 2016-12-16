from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.template.loader import get_template

import re

from .forms import ContactForm
from spiders.run_spiders import run_spiders
from scrape_games.models import HitCount

def run_scrapers(key, excluded):
    spider_list = run_spiders(key, excluded)
    return spider_list

def filter_list(store_query_list):

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
                    if prevgame['faketitle'] == fake_title and game['price'] < prevgame['price']:
                        output_list.remove(prevgame)
                        output_list.append(game)

    return output_list

def home_page(request):
    try:
        pagehits = HitCount.objects.all()[0]
        pagehits.hits += 1
        pagehits.save()
    except IndexError:
        pagehits = HitCount()
        pagehits.hits = 0
        pagehits.save()
    messages.get_messages(request)
    return render(request, 'scrape_games_frontend/home.html', {'pagehits': pagehits,})


def games_page(request):

    if request.method == 'GET':
        key = request.GET.get("q")
        key = re.sub(r'[^\s\w]', '', key)
        excluded = request.GET.get("filters")
        print (request.get_full_path().split('/')[-1])
        if key.strip() == '':
            messages.add_message(request, messages.ERROR, "You must search for something.")
            return redirect(home_page)
    cache_key = request.get_full_path().split('/')[-1]
    if cache.get(cache_key+'output_list'):
        output_list = cache.get(cache_key+'output_list')
        store_query_list = cache.get(cache_key+'store_query_list')
        if request.path.endswith('as_json'):
            return JsonResponse(output_list, safe=False)
        else:
            return render(request, 'scrape_games_frontend/search_results.html', {
                'output_list': output_list,
                'store_query_list': store_query_list,
            })

    store_query_list, offline = run_scrapers(key, excluded)

    output_list = filter_list(store_query_list)
    output_list = sorted(output_list, key=lambda k: k['title'])
    if output_list:
        if not offline:
            cache.set(cache_key+'store_query_list',store_query_list, 60*10)
            cache.set(cache_key + 'output_list', output_list, 60 * 10)

        if request.path.endswith('as_json'):
            return JsonResponse(output_list, safe=False)

        return render(request, 'scrape_games_frontend/search_results.html', {
                                                                        'output_list': output_list,
                                                                        'store_query_list': store_query_list,
                                                                        'offline': offline,
                                                                        })

    else:
        messages.add_message(request, messages.ERROR, "There were no results.")
        return redirect(home_page)

def contact_me_page(request):

    contact_form = ContactForm

    if request.method == 'POST':
        form = contact_form(data=request.POST)
        if form.is_valid():
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')
            subject = request.POST.get('subject', '')
            content = request.POST.get('content', '')

            template = get_template('contact_template.txt')

            email = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'subject': subject,
                'content': content,
            }
            email_skel = template.render(email)

            email_message = EmailMessage(
                subject,
                email_skel,
                'SG',
                ['sendtosgdev@gmail.com'],
                headers={'Reply-To': contact_email}
            )

            email_message.send()
            messages.add_message(request, messages.INFO, "Message sent. Thank you for your feedback!")
            return redirect('contact_me')

    return render(request, 'scrape_games_frontend/contact_me.html', {})

