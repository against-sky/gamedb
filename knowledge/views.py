# coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse
from pymongo import *
from mysolr import Solr
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
import simplejson
# Create your views here.
mongo_url = 'mongodb://10.76.0.137:27017/'
# mongo_url = 'mongodb://localhost:27017'
client = MongoClient(mongo_url)
db = client['gamedb']
solr_url = 'http://localhost:8983/solr/'
baidu = client['baidu']

solr = Solr(solr_url)

@csrf_exempt
def getit(reqeust):
	url = reqeust.POST['url']
	d = {}
	d["ee"] = url
	d = {
		"name": "flare",
		"children": [
			{ "name": "analytics","size": 3938 ,"attr":"nihao"},
			{"name": "AgglomerativeCluster", "size": 3938, "attr":"dsljflaskdj"},
			{"name": "CommunityStructure", "size": 3812},
			{"name": "HierarchicalCluster", "size": 6714},
			{"name": "MergeEdge", "size": 743}
			]
		}

	d = simplejson.dumps(d)
	return HttpResponse(d,mimetype='application/javascript')


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
	searchtext = get_value(reqeust,'searchtext','')
	if searchtext =='' :
		return render(reqeust, 'knowledge/advance.html', {})
	else:
		name = 'name:' + searchtext
		query = {'q':name }
		response = solr.search(**query)
		doc = response.documents
		length = len(doc)
		print length
		if length == 0:
			pass
		else:
			game = baidu.baike.find({'_id':doc[0]['id']})
			page = dict(game[0])
 			page['id'] = game[0]['_id']
			print game[0]['iconLink']
			print page['id']
			print game[0]['name']
		return render(reqeust,'knowledge/adsearch.html',{ 'searchtext':searchtext, 'page':doc[0],'doc':doc[1:] ,'baike':page})


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
	# searchtext = get_value(reqeust,'searchtext','')
	return advance(reqeust)
	# return render(reqeust, 'knowledge/adsearch.html', { 'searchtext':searchtext })