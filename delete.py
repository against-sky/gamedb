# coding=utf-8
# delete 
from mysolr import Solr

solr_url = 'http://localhost:8983/solr/'

solr = Solr(solr_url)
query = {'q':'*:*'}
solr.delete_by_query(query,commit=True)