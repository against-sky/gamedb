# coding=utf-8
# delete 
from mysolr import Solr
#update lixiaoyao
#db.baike.update({_id:"http://baike.baidu.com/view/4488.htm"},{$set:{gameURL:["http://baike.baidu.com/subview/2188/5215542.htm" ]}})

solr_url = 'http://10.76.0.137:8983/solr/'
iden = [
	"http://baike.baidu.com/view/760101.htm",
	"http://baike.baidu.com/subview/10941/5236539.htm",
	"http://baike.baidu.com/subview/3049782/11262117.htm",
	"http://baike.baidu.com/subview/10786/6081536.htm",
	"http://baike.baidu.com/subview/533601/8190340.htm",
	"http://baike.baidu.com/view/1016334.htm",
	"http://baike.baidu.com/view/2106174.htm",
	"http://baike.baidu.com/subview/187895/6353044.htm",
	"http://baike.baidu.com/subview/187895/6353038.htm",
	"http://baike.baidu.com/view/123796.htm",
	"http://baike.baidu.com/subview/187895/6353044.htm",
	"http://baike.baidu.com/subview/168512/7010262.htm",	
]


solr = Solr(solr_url)
for x in iden:
	solr.delete_by_key(x,commit=True)

'''
query = {'q':'*:*'}
solr.delete_by_query(query,commit=True)
'''
