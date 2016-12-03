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

        key = re.sub(r'[^\s\w]', '', key)
        cache_key = key.replace(' ', '').lower()
        if cache.get(cache_key + 'output_list'):
            output_list = cache.get(cache_key + 'output_list')
            store_query_list = cache.get(cache_key + 'store_query_list')
            if game_id != None:
                out = self.selected_game(store_query_list, output_list[game_id]['faketitle'])
                return Response(out)

            return Response(output_list)

        store_query_list, offline = self.run_scrapers(key)
        output_list = self.filter_list(store_query_list)

        if output_list and not offline:
            cache.set(cache_key + 'store_query_list', store_query_list, 60 * 10)
            cache.set(cache_key + 'output_list', output_list, 60 * 10)
        if game_id != None:
            out = self.selected_game(store_query_list, output_list[game_id]['faketitle'])
            return Response(out)
        return Response(output_list)

    def run_scrapers(self, key):
        spider_list = run_spiders(key)
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
