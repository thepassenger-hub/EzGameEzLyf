from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from spiders.run_spiders import run_spiders
import re

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
                return Response(out)
            return Response(output_list)
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
                    return Response(out)
                return Response(output_list)



        store_query_list, offline = self.run_scrapers(key, excluded)
        output_list = self.filter_list(store_query_list)

        if output_list and not offline:
            cache.set(cache_key + '+store_query_list', store_query_list, 60 * 10)
            cache.set(cache_key + '+output_list', output_list, 60 * 10)
        if game_id is not None:
            out = self.selected_game(store_query_list, output_list[game_id]['faketitle'])
            return Response(out)
        return Response(output_list)

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
