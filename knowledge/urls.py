from django.conf.urls import patterns, url
from knowledge import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^search/', views.search, name='search'),
)