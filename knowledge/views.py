# coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse
from pymongo import *

# Create your views here.
mongo_url = 'mongodb://10.76.0.137:27017/'
# mongo_url = 'mongodb://localhost:27017'
client = MongoClient(mongo_url)
db = client['gamedb']

def get_value(reqeust,key,default):
	if key in reqeust.GET and reqeust.GET[key].strip() != '':
		return reqeust.GET[key].strip()
	else:
		return default

def index(reqeust):
	print 'this is index'
	return render(reqeust, 'knowledge/index.html', {})

def advance(reqeust):
	print 'this is advance'
	return render(reqeust, 'knowledge/advance.html', {})

def about(reqeust):
	print 'this is about'
	return render(reqeust, 'knowledge/about.html', {})


def search(reqeust):
	searchtext = get_value(reqeust,'searchtext','')
	print 'this is search reqeust'
	if searchtext != '':
		gamedata = db.library.find_one({'name':searchtext })
		if gamedata:
			pass
		else:
			gamedata = None
	else:
		return render(reqeust, 'knowledge/index.html', {})

	return render(reqeust, 'knowledge/search.html', {'searchtext':searchtext, 'gamedata':gamedata })

def adsearch(reqeust):
	searchtext = get_value(reqeust,'searchtext','')
	return render(reqeust, 'knowledge/adsearch.html', { 'searchtext':searchtext })