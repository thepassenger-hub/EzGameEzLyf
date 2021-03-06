from django.conf.urls import url
from django.views.generic.base import RedirectView, TemplateView
from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url = 'index/', permanent = False), name = 'index'),
    url(r'^index', views.home_page, name = 'home'),
    url(r'^search/$', views.games_page, name = 'search'),
    url(r'^search/as_json$', views.games_page, name = 'search_as_json'),
    url(r'^faq', TemplateView.as_view(template_name = 'scrape_games_frontend/faq.html'), name = 'faq'),
    url(r'^contactme', views.contact_me_page, name = 'contact_me'),

]