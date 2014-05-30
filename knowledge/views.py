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
solr_url = 'http://10.76.0.137:8983/solr/'
#solr_url = 'http://localhost:8983/solr/'
#mongo_url = 'mongodb://localhost:27017'

client = MongoClient(mongo_url)
db = client['knowledge']
baidu = client['baidu']

solr = Solr(solr_url)

def getGraph(url):
	tree = baidu.tree.find({'_id':url})[0]
	print 'begin'
	print tree['name'].encode('utf-8'),tree['attr'].encode('utf-8')
	print 'mid'
	print len(tree['children'])
	print 'end'
	return tree

@csrf_exempt
def getit(reqeust):
	url = reqeust.POST['url']

	tree = baidu.tree.find_one({ '_id':url })
	#tree = getGraph(url)
	# d = {}
	d = { "name": "No Graph" }
	#print tree.name,tree['attr']
	print 'get tree'
	if tree:
		'''
		d = {}
		d['name'] = tree['name']
		children = tree['children']
		print 'a'
		print len(children)
		print 'b'
		'''
		tree = tree['tree']
		print len(tree['children'])
		if len(tree['children'])>50:
			tree['children'] = tree['children'][0:50]
		# print tree
		d = simplejson.dumps(tree)
	else:
		d = simplejson.dumps(d)
	#print d
	return HttpResponse(d,mimetype='application/javascript')


def get_value(reqeust,key,default):
	if key in reqeust.GET and reqeust.GET[key].strip() != '':
		return reqeust.GET[key].strip()
	else:
		return default

def game(reqeust, param1):
	#print param1
	gamedata = db.wangluo.find_one({'_id':param1 })
	if gamedata:
		companygames = db.wangluo.find({'developer':gamedata['developer'],'_id':{ '$not': re.compile(gamedata['_id'])}},{'originalURL':1,'name':1,'subType':1,'iconLink':1}).limit(40)
		similargames = db.wangluo.find({'_id':{'$in':gamedata['similarGames']}},{'originalURL':1,'name':1,'subType':1,'iconLink':1})
		#print gamedata['similarGames']
		#for x in similargames:
		#	print x['_id']
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
	res = getSimilarNames(searchtext,int(checked),3.0)
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
	# res = getFromSolr(searchtext,int(checked),3.0)
	if res:
		pass
	else:
		return None,None,None,None
	#print res
	gamedata = collection.find_one({'_id':res[0]['id']})
	similarNames = res[1:]
	#print similarNames
	if gamedata:
		companygames = collection.find({'developer':gamedata['developer'],'_id':{ '$not': re.compile(gamedata['_id'])}},{'originalURL':1,'name':1,'subType':1,'iconLink':1}).limit(40)
		similargames = collection.find({'_id':{'$in':gamedata['similarGames']}},{'originalURL':1,'name':1,'subType':1,'iconLink':1})
		return gamedata, companygames, similargames, similarNames
	else:
		return None, None, None, None
		

def index(reqeust):
	print 'this is index'
	return render(reqeust, 'knowledge/index.html', {})

def getSimilarNames(searchtext,nameType,threshold):
	name = ''
	if nameType == 0:
		name = 'name:'
		fl = 'id,name,score'
	elif nameType == 1:
		name = 'wlname:'
		fl = 'id,wlname,score'
	elif nameType == 2:
		name = 'wyname:'
		fl = 'id,wyname,score'
	elif nameType == 3:
		name = 'djname:'
		fl = 'id,djname,score'
	elif nameType == 4:
		name = 'adname:'
		fl = 'id,adname,score'
	elif nameType == 5:
		name = 'ipname:'
		fl = 'id,ipname,score'
	name = name + searchtext
	query = {'q':name,'fl':fl}
	doc = solr.search(**query).documents
	#print doc
	res = []
	for item in doc:
		if item['score'] > threshold:
			dic = {}
			dic['id'] = item['id']
			if nameType == 1:
				dic['name'] = item['wlname']
			elif nameType == 2:
				name = 'wyname:'
				dic['name'] = item['wyname']
			elif nameType == 3:
				name = 'djname:'
				dic['name'] = item['djname']
			elif nameType == 4:
				name = 'adname:'
				dic['name'] = item['adname']
			elif nameType == 5:
				name = 'ipname:'
				dic['name'] = item['ipname']
			res.append(dic)
	return res

def getFromSolr(searchtext,nameType,threshold):
	name = ''
	if nameType == 0:
		name = 'name:'
		fl = 'id,name,score'
	elif nameType == 1:
		name = 'wlname:'
		fl = 'id,wlname,score'
	elif nameType == 2:
		name = 'wyname:'
		fl = 'id,wyname,score'
	elif nameType == 3:
		name = 'djname:'
		fl = 'id,djname,score'
	elif nameType == 4:
		name = 'adname:'
		fl = 'id,adname,score'
	elif nameType == 5:
		name = 'ipname:'
		fl = 'id,ipname,score'
	name = name + searchtext
	query = {'q':name,'fl':fl}
	doc = solr.search(**query).documents
	#print doc
	res = []
	for item in doc:
		if item['score'] > threshold:
			res.append(item['id'])
	#return res
	if res:
		return res
	else:
		for x in doc:
			res.append(x['id'])

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
		is_role = False
		other = []
		tmp = getFromSolr(searchtext,0,3.0)
		tmpsearchtext = searchtext
		if tmp:
			page = baidu.baike.find_one({'_id':tmp[0]})
			print page['pagetype']
			# print page['gameURL']
			
			print tmp[0]
			if page.has_key('gameURL') and page['pagetype'] == '0':
				other  = baidu.baike.find({'_id':{'$in':page['gameURL']}},{'_id':1,'name':1,'summary':1,'titles':1,'originalURL':1,'basic':1})
				# print other[0]['name']
				# print other[0]['name']
				if other.count()>0:
					tmpsearchtext = other[0]['name']
					is_role = True
			else:
				if len(tmp)>1:
					other  = baidu.baike.find({'_id':{'$in':tmp[1:]}},{'_id':1,'name':1,'summary':1,'titles':1,'originalURL':1})
				# tree = baidu.tree.find_one({ '_id':tmp[0] })
				# if tree:
					# print tree
					# pass

		else:
			page = None
		
		#print other
		tmp = getFromSolr(tmpsearchtext,1,3.0)
		if tmp:
			gamewangluo = db.wangluo.find_one({'_id':tmp[0]})

		else:
			gamewangluo = None
		tmp = getFromSolr(tmpsearchtext,2,3.0)
		if tmp:
			gamewangye = db.wangye.find_one({'_id':tmp[0]})
		else:
			gamewangye = None
		tmp = getFromSolr(tmpsearchtext,3,3.0)
		if tmp:
			gamedanji = db.danji.find_one({'_id':tmp[0]})
		else:
			gamedanji = None
		tmp = getFromSolr(tmpsearchtext,4,3.0)
		if tmp:
			gameandroid = db.android.find_one({'_id':tmp[0]})
		else:
			gameandroid = None
		tmp = getFromSolr(tmpsearchtext,5,3.0)
		if tmp:
			gameiphone = db.iphone.find_one({'_id':tmp[0]})
		else:
			gameiphone = None
		# name = 'name:' + searchtext
		# gamewangluo = db.wangluo.find_one({'name':{'$regex':searchtext}})
		# gamewangye = db.wangye.find_one({'name':{'$regex':searchtext}})
		# gamedanji = db.danji.find_one({'name':{'$regex':searchtext}})
		# gameandroid = db.android.find_one({'name':searchtext})
		# gameiphone = db.iphone.find_one({'name':searchtext})
		# query = {'q':name }
		# response = solr.search(**query)
		# doc = response.documents
		# length = len(doc)
		# page = None
		# print length
		# if length == 0:
		# 	pass
		# else:
		# 	game = baidu.baike.find({'_id':doc[0]['id']})

			

		# 	page = dict(game[0])
 	# 		page['id'] = game[0]['_id']
		# 	print page['id']
		return render(reqeust,'knowledge/adsearch.html',{ 
			'searchtext':searchtext, 
			'gamewangluo':gamewangluo,
			'gamewangye':gamewangye,
			'gamedanji':gamedanji,
			'gameandroid':gameandroid,
			'gameiphone':gameiphone,
			'baike':page,
			'other':other,
			'is_role':is_role})


def about(reqeust):
	print 'this is about'
	return render(reqeust, 'knowledge/about.html', {})


def search(reqeust):
	searchtext = get_value(reqeust,'searchtext','')
	checked = get_value(reqeust,'radio','4')
	#print type(checked)
	#print checked
	print 'this is search reqeust'
	if searchtext != '':
		gamedata, companygames, similargames, similarNames = getgame(searchtext,checked)

	else:
		return render(reqeust, 'knowledge/index.html', {})

	return render(reqeust, 'knowledge/search.html', {
		'searchtext':searchtext,
		'checked':checked, 
		'gamedata':gamedata, 
		'companygames':companygames, 
		'similargames':similargames,
		'similarNames':similarNames })

def adsearch(reqeust):
	# searchtext = get_value(reqeust,'searchtext','')
	return advance(reqeust)
	# return render(reqeust, 'knowledge/adsearch.html', { 'searchtext':searchtext })
