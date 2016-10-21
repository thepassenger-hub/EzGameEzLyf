from django.conf.urls import url
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url = 'index/', permanent = False), name = 'index'),
    url(r'index', views.home_page, name = 'home'),
    url(r'^search/$', views.games_page, name = 'search'),
    url(r'^search/game/$', views.selected_game, name = 'selected_game'),

]