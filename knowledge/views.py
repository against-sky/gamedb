# coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse
from pymongo import *

# Create your views here.
client = MongoClient()
db = client['gamedb']

def get_value(reqeust,key,default):
	if key in reqeust.GET and reqeust.GET[key].strip() != '':
		return reqeust.GET[key].strip()
	else:
		return default

def index(reqeust):
	print 'this is index'
	return render(reqeust, 'knowledge/index.html', {})

def search(reqeust):
	searchtext = get_value(reqeust,'searchtext','')
	print 'this is search reqeust'
	print searchtext
	# if searchtext == '':
	# 	return render(reqeust, 'knowledge/index.html', {})
	# else:
	if searchtext != '':
		gamedata = db.library.find_one({'name':searchtext })
		# if gamedata:
	print gamedata['name']
	return render(reqeust, 'knowledge/search.html', {'searchtext':searchtext, 'gamedata':gamedata })