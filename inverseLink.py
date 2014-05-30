from pymongo import *
client = MongoClient()
db = client['baidu']

print 'add originalURL'
'''
allpages = db.baike.find()
count = 0
for x in allpages:
	print count
	count = count + 1
	db.baike.update({'_id':x['_id']},{'$set':{'originalURL':x['_id']}})
'''
print 'delete role--game relation'
db.baike.update({},{'$unset':{'gameURL':1}},multi=True)

print 'construct role-->game relation'
count = 0
allpages = db.baike.find({'pagetype':'1'},{'_id':1,'name':1,'outlinks':1})
print allpages.count()
for page in allpages:
	if page.has_key('outlinks'):
		print count
		count = count + 1
		outlinks = page['outlinks']
		for link in outlinks:
			db.baike.update({'_id':link,'pagetype':'0'},{'$push':{'gameURL':page['_id']}})

print 'update attr'
allpages = db.baike.find({},{'_id':1,'name':1,'tags':1})
print allpages.count()

for page in allpages:
	#print page['name'].encode('utf-8')
	if page.has_key('tags'):
		print page['_id']
		attr = ''
		cnt = -1
		if len(page['tags'])==1:
			attr = page['tags'][0]
		elif len(page['tags']) == 2:
			attr = page['tags'][0]+','+page['tags'][1]
		elif len(page['tags']) >= 3:
			attr = page['tags'][0]+','+page['tags'][1]+','+page['tags'][2]
		print attr.encode('utf-8')
		db.baike.update({'_id':page['_id']},{'$set':{'attr':attr}})

print 'construct db invserse'
allpages = db.baike.find({},{'_id':1,'outlinks':1})
print allpages.count()
#db.inverse.remove({})
count = 0
for page in allpages:
	source = str(page['_id'])
	if source.startswith('http'):
		pass
	else:
		continue
	count = count + 1
	print count

	if page.has_key('outlinks'):
		print page['_id']
		print len(page['outlinks'])
		for x in page['outlinks']:
			db.inverse.insert({
				'from':page['_id'],
				'to':x
			})

print 'construct tree for each node'
allpages = db.baike.find({},{'_id':1,'name':1,'attr':1,'pagetype':1,'outlinks':1})
count = 1
for page in allpages:
	d = {}
	if str(page['_id']).startswith('http'):
		pass
	else:
		continue
	
	d['name'] = page['name']
	if page.has_key('attr'):
		print count
		count = count + 1
		d['attr'] = page['attr']
	
	children = []
	tmp = ''
	outlinks = []
	if page['pagetype'] == '1':
		#if page.has_key('outlinks'):
		outlinks = page['outlinks']
		
		print len(outlinks)
		#print len(page['outlinks'])
		print page['name'].encode('utf-8')
	#	##tmp = db.baike.find({'_id':{'$in':outlinks}},{'name':1,'tags':1})
	else:
		froms = db.inverse.find({'to':page['_id']})
		outlinks = []
		for item in froms:
			outlinks.append(item['from'])
	tmp = db.baike.find({'_id':{'$in':outlinks}},{'name':1,'attr':1})
	for item in tmp:
		child = {}
		child['name'] = item['name']
		attr = ''
		if item.has_key('attr'):
			child['attr'] = item['attr']
			children.append(child)
	d['children'] = children
	db.tree.save({'_id':page['_id'],'tree':d})
	#else:
		#tos = db.inverse.find('from':page['_id'])
		#tmp = db.baike




'''
for page  in allpages:
	source = str(page['_id'])
	#print source
	#continue

	if source.startswith('http'):
		#source = page['_id']
		print count
		count = count + 1
		outlinks = page['outlinks']
		for link in outlinks:
			db.inverse.insert({
				'from':link,
				'to':source
			})

'''
