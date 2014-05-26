from pymongo import *
client = MongoClient()
db = client['baidu']

allpages = db.baike.find()
count = 1
for page in allpages:
	d = {}
	d['name'] = page['name']
	if page.has_key('tags'):
		print count
		count = count + 1
		attr = ''
		for x in page['tags']:
			attr = attr + x + ','
		d['attr'] = attr
		pass
	else:
		continue
	children = []
	tmp = ''
	if page['pagetype'] == '1':
		#children = []
		outlinks = page['outlinks']
		#tmp = db.baike.find({'_id':{'$in':outlinks}},{'name':1,'tags':1})
	else:
		tos = db.inverse.find({'from':page['_id']})
		outlinks = []
		for item in tos:
			outlinks.append(item['to'])
	tmp = db.baike.find({'_id':{'$in':outlinks}},{'name':1,'tags':1})
	for item in tmp:
		child = {}
		child['name'] = item['name']
		attr = ''
		if item.has_key('tags'):
			for x in item['tags']:
				attr = attr + x + ','
			child['attr'] = attr
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
