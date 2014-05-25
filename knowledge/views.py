# coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse
from pymongo import *
from mysolr import Solr
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
import simplejson
import re
# Create your views here.
mongo_url = 'mongodb://10.76.0.137:27017/'
# mongo_url = 'mongodb://localhost:27017'
client = MongoClient(mongo_url)
db = client['knowledge']
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

def game(reqeust, param1):
	print param1
	gamedata = db.wangluo.find_one({'_id':param1 })
	if gamedata:
		companygames = db.wangluo.find({'developer':gamedata['developer'],'_id':{ '$not': re.compile(gamedata['_id'])}},{'originalURL':1,'name':1,'subType':1,'iconLink':1}).limit(40)
		similargames = db.wangluo.find({'_id':{'$in':gamedata['similarGames']}},{'originalURL':1,'name':1,'subType':1,'iconLink':1})
		return render(reqeust, 'knowledge/search.html', {'searchtext':gamedata['name'],'checked':'1', 'gamedata':gamedata,'companygames':companygames ,'similargames':similargames})
	gamedata = db.wangye.find_one({'_id':param1 })
	if gamedata:
		companygames = db.wangye.find({'developer':gamedata['developer'],'_id':{ '$not': re.compile(gamedata['_id'])}},{'originalURL':1,'name':1,'subType':1,'iconLink':1}).limit(40)
		similargames = db.wangye.find({'_id':{'$in':gamedata['similarGames']}},{'originalURL':1,'name':1,'subType':1,'iconLink':1})
		return render(reqeust, 'knowledge/search.html', {'searchtext':gamedata['name'], 'checked':'2','gamedata':gamedata,'companygames':companygames ,'similargames':similargames})
	gamedata = db.danji.find_one({'_id':param1 })
	if gamedata:
		companygames = db.danji.find({'developer':gamedata['developer'],'_id':{ '$not': re.compile(gamedata['_id'])}},{'originalURL':1,'name':1,'subType':1,'iconLink':1}).limit(40)
		similargames = db.danji.find({'_id':{'$in':gamedata['similarGames']}},{'originalURL':1,'name':1,'subType':1,'iconLink':1})
		return render(reqeust, 'knowledge/search.html', {'searchtext':gamedata['name'],'checked':'3', 'gamedata':gamedata,'companygames':companygames ,'similargames':similargames})
	gamedata = db.android.find_one({'_id':param1 })
	if gamedata:
		companygames = db.android.find({'developer':gamedata['developer'],'_id':{ '$not': re.compile(gamedata['_id'])}},{'originalURL':1,'name':1,'subType':1,'iconLink':1}).limit(40)
		similargames = db.android.find({'_id':{'$in':gamedata['similarGames']}},{'originalURL':1,'name':1,'subType':1,'iconLink':1})
		return render(reqeust, 'knowledge/search.html', {'searchtext':gamedata['name'], 'checked':'4','gamedata':gamedata,'companygames':companygames ,'similargames':similargames})
	gamedata = db.iphone.find_one({'_id':param1 })
	if gamedata:
		companygames = db.iphone.find({'developer':gamedata['developer'],'_id':{ '$not': re.compile(gamedata['_id'])}},{'originalURL':1,'name':1,'subType':1,'iconLink':1}).limit(40)
		similargames = db.iphone.find({'_id':{'$in':gamedata['similarGames']}},{'originalURL':1,'name':1,'subType':1,'iconLink':1})
		return render(reqeust, 'knowledge/search.html', {'searchtext':gamedata['name'], 'checked':'5','gamedata':gamedata,'companygames':companygames ,'similargames':similargames})	
	return render(reqeust, 'knowledge/index.html', {})

def getgame(searchtext, checked):
	print 'in get game',checked
	if checked == '1':
		collection = db['wangluo']
	elif checked == '2':
		collection = db['wangye']
	elif checked == '3':
		collection = db['danji']
	elif checked == '4':
		collection = db['android']
	else:
		collection = db['iphone']
	gamedata = collection.find_one({'name':searchtext})
	if gamedata:
		companygames = collection.find({'developer':gamedata['developer'],'_id':{ '$not': re.compile(gamedata['_id'])}},{'originalURL':1,'name':1,'subType':1,'iconLink':1}).limit(40)
		similargames = collection.find({'_id':{'$in':gamedata['similarGames']}},{'originalURL':1,'name':1,'subType':1,'iconLink':1})
		return gamedata, companygames, similargames
	else:
		return None, None, None
		

def index(reqeust):
	print 'this is index'
	return render(reqeust, 'knowledge/index.html', {})

def advance(reqeust):
	print 'this is advance'
	searchtext = get_value(reqeust,'searchtext','')
	# gamewangluo = None
	# gamewangye = None
	# gamedanji = None
	# gameandroid = None
	# gameiphone = None

	if searchtext =='' :
		return render(reqeust, 'knowledge/advance.html', {})
	else:
		name = 'name:' + searchtext
		gamewangluo = db.wangluo.find_one({'name':{'$regex':searchtext}})
		gamewangye = db.wangye.find_one({'name':{'$regex':searchtext}})
		gamedanji = db.danji.find_one({'name':{'$regex':searchtext}})
		gameandroid = db.android.find_one({'name':searchtext})
		gameiphone = db.iphone.find_one({'name':searchtext})
		query = {'q':name }
		response = solr.search(**query)
		doc = response.documents
		length = len(doc)
		page = None
		print length
		if length == 0:
			pass
		else:
			game = baidu.baike.find({'_id':doc[0]['id']})

			

			page = dict(game[0])
 			page['id'] = game[0]['_id']
			print page['id']
		return render(reqeust,'knowledge/adsearch.html',{ 
			'searchtext':searchtext, 
			'gamewangluo':gamewangluo,
			'gamewangye':gamewangye,
			'gamedanji':gamedanji,
			'gameandroid':gameandroid,
			'gameiphone':gameiphone,
			'baike':page})


def about(reqeust):
	print 'this is about'
	return render(reqeust, 'knowledge/about.html', {})


def search(reqeust):
	searchtext = get_value(reqeust,'searchtext','')
	checked = get_value(reqeust,'radio','4')
	print type(checked)
	print checked
	print 'this is search reqeust'
	if searchtext != '':
		gamedata, companygames, similargames = getgame(searchtext,checked)

	else:
		return render(reqeust, 'knowledge/index.html', {})

	return render(reqeust, 'knowledge/search.html', {'searchtext':searchtext,'checked':checked, 'gamedata':gamedata, 'companygames':companygames, 'similargames':similargames })

def adsearch(reqeust):
	# searchtext = get_value(reqeust,'searchtext','')
	return advance(reqeust)
	# return render(reqeust, 'knowledge/adsearch.html', { 'searchtext':searchtext })