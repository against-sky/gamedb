from django.conf.urls import patterns, url
from knowledge import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^advance$', views.advance, name='advance'),
	url(r'^adsearch$', views.adsearch, name='adsearch'),
	url(r'^about$', views.about, name='about'),
	url(r'^search$', views.search, name='search'),
)