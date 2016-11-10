from django.conf.urls import url
from django.views.generic.base import RedirectView, TemplateView
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url = 'index/', permanent = False), name = 'index'),
    url(r'index', views.home_page, name = 'home'),
    url(r'^search/$', cache_page(60*10)(views.games_page), name = 'search'),
    url(r'^search/game/$', views.selected_game, name = 'selected_game'),
    url(r'^faq', TemplateView.as_view(template_name = 'scrape_games_frontend/faq.html'), name = 'faq'),
    url(r'^contactme', views.contact_me_page, name = 'contact_me'),

]