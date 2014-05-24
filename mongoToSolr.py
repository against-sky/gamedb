# coding=utf-8

from pymongo import *
from mysolr import Solr

mongo_url = 'mongodb://10.76.0.137:27017/'
# mongo_url = 'mongodb://localhost:27017'
client = MongoClient(mongo_url)
db = client['baidu']

solr_url = 'http://localhost:8983/solr/'

solr = Solr(solr_url)


pages = db.baike.find().limit(100)
items = []

count = 0

for page in pages:
	print count
	count = count + 1
	item = {}
	if page.has_key('subname'):
		pass
	else:
		continue
		
	print page['name']
	print page['subname']
	print page['_id']

	item['id'] = page['_id']
	item['name'] = page['name']
	item['subname'] = page['subname']
	item['content'] = page['content']
	items.append(item)

solr.update(items, 'json',commit=False)
solr.commit()

'''
items = []

for index in xrange(11,16):
	game = games[index]
	item = {}
	item['bname'] = game['name']
	item['bsummary'] = game['des']
	item['id'] = game['url']
	tmp = ''
	for x in game['property']:
		tmp = tmp + x['title']+':'
		tmp = tmp + x['content']+'\n'
	item['bcontent'] = tmp

	#print item['content']
	print item['bname']
	print item['id']
	items.append(item)

solr.update(items, 'json',commit=False)

solr.commit()
'''


