import couchdb
import json
import os
from pathlib import Path


#CouchDB authentication
COUCHDB_SERVER='http://admin:admin@172.26.132.158:49186/'
DBNAME = 'lsy_test'
couch = couchdb.Server(COUCHDB_SERVER)
db = couch[DBNAME]



with open('upload_sample.txt') as f:
    count = 0
    for line in f:
        data = json.loads(line)
        db.save(data)
        if count == 0:
            print(data)
        count += 1