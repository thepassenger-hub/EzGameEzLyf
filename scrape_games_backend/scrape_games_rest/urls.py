from django.conf.urls import url, include
from scrape_games_rest.views import GamesOutput

urlpatterns = [
    url(r'^search/$', GamesOutput.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]