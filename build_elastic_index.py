FILE_URL="https://s3.amazonaws.com/h2o-public-test-data/smalldata/gbm_test/titanic.csv"
#data can also be stored in amazon S3 bucket

ES_HOST={"host":"localhost","port":9200}
INDEX_NAME='titanic'
TYPE_NAME='passenger'
ID_FIELD='passengerid'

import csv
import urllib2

response=urllib2.urlopen(FILE_URL)
csv_reader=csv.reader(response)

header=csv_reader.next()
header=[item.lower() for item in header]
print header
data_bulk=[]
cnt=0
for row in csv_reader:
	cnt=cnt+1
	data_dict={}
	for i in range(len(row)):
		data_dict[header[i]]=row[i]
	ind_dict={	
			"index": { 
					"_index":INDEX_NAME,
					"_type":TYPE_NAME,
					"_id":cnt
				 }
		}
	data_bulk.append(ind_dict)
	data_bulk.append(data_dict)
print len(data_bulk)
#2618 rows

from elasticsearch import Elasticsearch

#creating ES Client
es=Elasticsearch(hosts=[ES_HOST])
if es.indices.exists(INDEX_NAME):
	
	res=es.indices.delete(index=INDEX_NAME)
	print("deleting existing index '%s' with response '%s'"%(INDEX_NAME,res))

#creating request
request_body={
		"settings": {
				"number_of_shards": 1,
				"number_of_replicas":0
			    }
	     }

#creating ES index
print("creating index '%s'"%(INDEX_NAME))
res=es.indices.create(index=INDEX_NAME,body=request_body)
print("created with response '%s'"%(res))

#populating index with data (bulk index)
print("bulk indexing starting")
res=es.bulk(index=INDEX_NAME,body=data_bulk,refresh=True)


print("bulk indexing response '%s'"%(res.keys())) #keys of the index

#query to test the index
res=es.search(index= INDEX_NAME,size=5,body={"query":{"match":{"age": "30"}}}) #1st five records of people aged 30 are retrieved
print("response of test query: ")
for hit in res['hits']['hits']:
	print(hit["_source"])





	
	
	



