import couchdb
import json
import requests


COUCHDB_SERVER='http://admin:admin@172.26.128.214:5984/'
DBNAME = 'tiny_sample'
couch = couchdb.Server(COUCHDB_SERVER)
db = couch[DBNAME]

full_text_search_payload = {
  "_id": "_design/textsearch/text",
  "indexes": {
    "text": {
      "index": "function (doc) { index(\"default\", doc._id); index ('text', doc.text, {store: true}); index ('language', doc.lang, {facet: true, store: true});}"
    }
  }
}

def upload2couchDB(row):
    if type(row) == dict:
        db.save(row)
    else:
        data = json.loads(row)
        db.save(data)


def get_view(design_doc, view_name, group_level = '0', reduce = 'true'):
    return db.view(design_doc + '/' + view_name, group_level = group_level, reduce = reduce)

def post_index(payload):
    url = COUCHDB_SERVER + DBNAME + '/_index'
    headers = {"Content-Type": "application/json"}
    if type(payload) != dict:
        raise TypeError('data has to be a dict')
    return json.loads(requests.post(
        url, 
        data = json.dumps(payload), 
        headers = headers)
        .content.decode("utf-8"))

def get_index():
    return db.index()

def put_text_search(payload = full_text_search_payload, design_doc = 'textsearch'):
    url = COUCHDB_SERVER + DBNAME + '/_design' + '/' + design_doc
    headers = {"Content-Type": "application/json"}
    if type(payload) != dict:
        raise TypeError('data has to be a dict')
    return json.loads(requests.put(
        url, 
        data = json.dumps(payload), 
        headers = headers)
        .content.decode("utf-8"))

def search_query(query, design_doc = 'textsearch', index_name = 'text'):
    url = COUCHDB_SERVER + DBNAME + '/_design/' + 'design_doc' + '/_search/' + index_name
    headers = {"Content-Type": "application/json"}
    if type(query) != dict:
        raise TypeError('data has to be a dict')
    return json.loads(requests.post(
        url, 
        data = json.dumps(query), 
        headers = headers)
        .content.decode("utf-8"))

def map_reduce_fuc():
    url = 'http://admin:admin@172.26.128.214:5984/' + DBNAME + '/_design/city_covid'
    map_func = "function(doc) {{\
            var re = /covid|coronavirus|corona|cov19|corona|virus|cov |isolation|lockdown/;\
            if(re.test(doc.text.toLowerCase()))\
            emit([doc.place.name],1);\
        }\
    }"
    reduce_func = " function (key, values, rereduce) { return sum(values); }"
    data = {"views": {"filter_covid":
                          {"map": map_func,
                           "reduce": reduce_func
                           },
                      }}
    headers = {"Content-Type": "application/json"}
    r = requests.put(url, data=json.dumps(data), headers=headers)
    print(r.content)
    list_city = {}
    for item in db.view('city_covid/filter_covid', group_level='2', reduce='true'):

        print(item.key, item.id, item.value)

def map_reduce_subjectivity():
    url = 'http://admin:admin@172.26.128.214:5984/' + DBNAME + '/_design/city_subjectivity'
    map_func = "function (doc) {emit([doc.place.name],doc.subjectivity)};"
    reduce_func = " function (key, values, rereduce) { return sum(values); }"
    data = {"views": {"filter_sub":
                          {"map": map_func,
                           "reduce": reduce_func
                           },
                      }}
    headers = {"Content-Type": "application/json"}
    r = requests.put(url, data=json.dumps(data), headers=headers)
    print(r.content)
    list_city = {}
    for item in db.view('city_subjectivity/filter_sub', group_level='2', reduce='true'):
        print(item.key, item.id, item.value)

def map_reduce_polarity():
    url = 'http://admin:admin@172.26.128.214:5984/' + DBNAME + '/_design/city_polarity'
    map_func = "function (doc) {emit([doc.place.name],doc.polarity)};"
    reduce_func = " function (key, values, rereduce) { return sum(values); }"
    data = {"views": {"filter_pol":
                          {"map": map_func,
                           "reduce": reduce_func
                           },
                      }}
    headers = {"Content-Type": "application/json"}
    r = requests.put(url, data=json.dumps(data), headers=headers)
    print(r.content)
    list_city = {}
    for item in db.view('city_polarity/filter_pol', group_level='2', reduce='true'):
        print(item.key, item.value)


def map_reduce_city_num():
    url = 'http://admin:admin@172.26.128.214:5984/' + DBNAME + '/_design/city_num'
    map_func = "function (doc) {emit([doc.place.name],1)};"
    reduce_func = " function (key, values, rereduce) { return sum(values); }"
    data = {"views": {"city":
                          {"map": map_func,
                           "reduce": reduce_func
                           },
                      }}
    headers = {"Content-Type": "application/json"}
    r = requests.put(url, data=json.dumps(data), headers=headers)
    print(r.content)

    for item in db.view('city_num/city',group_level='2',reduce='true'):
        print(item.key, item.value)

