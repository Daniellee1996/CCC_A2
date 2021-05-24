import couchdb
import json
import requests


COUCHDB_SERVER='http://admin:admin@172.26.128.214:5984/'
DBNAME = 'twitter'
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



def map_covid():
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
    list_covid_city = {}


def map_subjectivity():
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


def map_polarity():
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



def map_city_num():
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




def reduce_city_num():
    city_num = {}
    for item in db.view('city_num/city',group_level='2',reduce='true'):
        city_num[item.key[0]] = item.value
        print(item.key, item.value)
    print(len(city_num))
    return city_num

#客观或者不客观
def reduce_subjectivity():
    city_subjectivity = {}
    for item in db.view('city_subjectivity/filter_sub', group_level='2', reduce='true'):
        city_subjectivity[item.key[0]] = item.value
        print(item.key, item.value)
    return city_subjectivity

#积极或者不积极
def reduce_polarity():
    city_polarity = {}
    for item in db.view('city_polarity/filter_pol', group_level='2', reduce='true'):
        city_polarity[item.key[0]] = item.value
        print(item.key, item.value)
    return city_polarity

def reduce_covid():
    list_covid_city={}
    for item in db.view('city_covid/filter_covid', group_level='2', reduce='true'):
        list_covid_city[item.key[0]] = item.value

        #print(item.key, item.value)
    return list_covid_city

def reduce_covid_time():
    list_covid_time = {}
    for item in db.view('covid_time/filter_covid_time', group_level='2', reduce='true'):
        date = item.key.split("-")
        print(date)
        time = date[0] + "-"+ date[1]
        if time not in list_covid_time:
            list_covid_time[time] = item.value
        else:
            list_covid_time[time] += item.value
    # print(list_covid_time)
    return list_covid_time

# reduce_subjectivity()
#AIzaSyA8dLQ86ztG_wG-kBqExUecpTFLomseRlA
#reduce_city_num()
reduce_covid_time()