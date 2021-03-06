from django.conf.urls import patterns, url
from knowledge import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^getit$',views.getit, name='getit'),
	url(r'^advance$', views.advance, name='advance'),
	url(r'^adsearch$', views.adsearch, name='adsearch'),
	url(r'^game/(.+)$',views.game, name='game'),
	url(r'^about$', views.about, name='about'),
	url(r'^search$', views.search, name='search'),
)