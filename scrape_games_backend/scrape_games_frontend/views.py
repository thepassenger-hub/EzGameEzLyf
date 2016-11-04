from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import get_template

import re

from .forms import ContactForm
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
                    if prevgame['faketitle'] == fake_title and game['price'] < prevgame['price']:
                        output_list.remove(prevgame)
                        output_list.append(game)

    return output_list

def home_page(request):

    messages.get_messages(request)
    return render(request, 'scrape_games_frontend/home.html')

def games_page(request):

    if request.method == 'GET':
        key = request.GET.get("q")
        key = re.sub(r'[^\s\w]', '', key)
        if key.strip() == '':
            messages.add_message(request, messages.ERROR, "You must search for something.")
            return redirect(home_page)

    store_query_list = run_scrapers(key)
    request.session['store_query_list'] = store_query_list

    output_list = filter_list(store_query_list, key)
    output_list = sorted(output_list, key=lambda k: k['title'])

    return render(request, 'scrape_games_frontend/search_results.html', {
                                                                        'output_list': output_list,
                                                                        'store_query_list': store_query_list,
                                                                        })

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
