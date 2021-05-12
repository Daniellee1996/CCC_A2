import couchdb
import json


COUCHDB_SERVER='http://admin:admin@172.26.132.158:49186/'
DBNAME = 'tiny_sample'
couch = couchdb.Server(COUCHDB_SERVER)
db = couch[DBNAME]




def upload2couchDB(row):
    if type(row) == dict:
        db.save(row)
    else:
        data = json.loads(row)
        db.save(data)