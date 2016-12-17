from django import template

register = template.Library()

@register.inclusion_tag('tag_single_deals_mobile.html')
@register.inclusion_tag('tag_single_deals.html')
def show_all_games(store_query_list, title):
    list_of_games = []

    for game_list in store_query_list:
        for game in game_list:
            fake_title = game['faketitle']
            if fake_title == title:
                list_of_games.append(game)

    list_of_games = sorted(list_of_games, key=lambda k: k['price'])

    return {'list_of_games': list_of_games}