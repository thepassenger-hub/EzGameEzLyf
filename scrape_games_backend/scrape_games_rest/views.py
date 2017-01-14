from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from spiders.run_spiders import run_spiders
import re
from django.core.mail import EmailMessage
from django.template.loader import get_template

from scrape_games_rest.serializers import ContactSerializer

class GamesOutput(APIView):

    def get(self, request):
        key = request.query_params.get("q")
        game_id = request.query_params.get("id")
        game_id = int(game_id) if game_id else None
        excluded = request.GET.get("filters")
        excluded = excluded.split(',') if excluded else None

        key = re.sub(r'[^\s\w]', '', key).strip()
        cache_key = '?' + request.get_full_path().split('?')[-1].strip('+').replace('%20', '+').replace(',', '%2C')
        cache_key = re.sub(r'&id=[0-9]+','', cache_key)
        basic_cache_key = cache_key.split('&filters')[0]
        if cache.get(cache_key + '+output_list'):
            output_list = cache.get(cache_key + '+output_list')
            store_query_list = cache.get(cache_key + '+store_query_list')
            if game_id is not None:
                out = self.selected_game(store_query_list, output_list[game_id]['faketitle'])
                return Response(out, status=status.HTTP_200_OK)
            return Response(output_list, status=status.HTTP_200_OK)
        if excluded:
            if cache.get(basic_cache_key+'+output_list'):
                output_list = cache.get(basic_cache_key + '+output_list')
                output_list = [x for x in output_list if x['store'] not in excluded]
                store_query_list = cache.get(basic_cache_key + '+store_query_list')
                store_query_list = [x for x in store_query_list if x and x[0]['store'] not in excluded]
                cache.set(cache_key + '+store_query_list', store_query_list, 60 * 10)
                cache.set(cache_key + '+output_list', output_list, 60 * 10)
                if game_id is not None:
                    out = self.selected_game(store_query_list, output_list[game_id]['faketitle'])
                    return Response(out, status=status.HTTP_200_OK)
                return Response(output_list, status=status.HTTP_200_OK)



        store_query_list, offline = self.run_scrapers(key, excluded)
        output_list = self.filter_list(store_query_list)

        if output_list:
            if not offline:
                cache.set(cache_key + '+store_query_list', store_query_list, 60 * 10)
                cache.set(cache_key + '+output_list', output_list, 60 * 10)
            if game_id is not None:
                out = self.selected_game(store_query_list, output_list[game_id]['faketitle'])
                return Response(out, status=status.HTTP_200_OK)
            return Response(output_list, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def run_scrapers(self, key, excluded):
        spider_list = run_spiders(key, excluded)
        return spider_list

    def filter_list(self, store_query_list):

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

    def selected_game(self, store_query_list, title):
        list_of_games = []

        for game_list in store_query_list:
            for game in game_list:
                fake_title = game['faketitle']
                if fake_title == title:
                    list_of_games.append(game)

        list_of_games = sorted(list_of_games, key=lambda k: k['price'])

        return list_of_games

class Email(APIView):
    def post(self, request):

        data = request.data
        serializer = ContactSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            contact_name = data['name']
            contact_email = data['email']
            subject = data['subject']
            content = data['content']

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
            return Response(status=status.HTTP_201_CREATED)
        else:
            out = {'error': 'Invalid Email. Try again.'}
            return Response(out, status=status.HTTP_406_NOT_ACCEPTABLE)

