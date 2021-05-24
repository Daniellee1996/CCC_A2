from flask import Flask, render_template, Response, request ,jsonify
import json
import couchdb
import json
import requests

app = Flask(__name__)

twitter_count = {"total": 0, "Adelaide": 0, "Melbourne": 0, "Mornington": 0, "Perth": 0, "Sydney": 0}



@app.route('/index')
def homepage():
    return render_template('index.html')
    
COUCHDB_SERVER='http://admin:admin@172.26.128.214:5984/'
DBNAME = 'tiny_sample'
couch = couchdb.Server(COUCHDB_SERVER)
db = couch[DBNAME]
def map_reduce_fuc():
    url = 'http://admin:admin@172.26.128.214:5984/' + DBNAME + '/_design/filter_city'
    map_func = "function(doc) {{\
            var re = /covid|coronavirus|corona|cov19|corona|virus|cov |isolation|lockdown/;\
            if(re.test(doc.text.toLowerCase()))\
            emit([doc.place.name],1);\
        }\
    }"
    reduce_func = " function (key, values, rereduce) { return sum(values); }"
    data = {"views": {"my_filter":
                          {"map": map_func,
                           "reduce": reduce_func
                           },
                      }}
    headers = {"Content-Type": "application/json"}
    r = requests.put(url, data=json.dumps(data), headers=headers)
    print(r.content)
    list_city = {}
    key = []
    value = []
    for item in db.view('new_doc/my_filter', group_level='2', reduce='true'):
        #print(item.key, item.id, item.value)
        key.append(item.key[0])
        value.append(item.value)

    list_city['city'] = key
    list_city['value'] = value

    j=json.dumps(list_city)
    print(j)
    return j

@app.route('/simple_page')
def simple_page():
    return render_template('simple_page.html')

@app.route('/shortcodes')
def shortcodes():
    return render_template('shortcodes.html')

@app.route('/view_city', methods = ['GET', 'POST'])
def get_view():
    return map_reduce_fuc()

@app.route('/refresh_count')
def refresh_count():
	global twitter_count
	return jsonify(
		total = twitter_count["total"],
		Adelaide = twitter_count["Adelaide"],
		Melbourne = twitter_count["Melbourne"],
		Morningtom = twitter_count["Mornington"],
        Perth = twitter_count["Perth"],
        Sydney = twitter_count["Sydney"])

if __name__ == "__main__":
    app.run(debug=True,port=5000)