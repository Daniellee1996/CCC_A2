from flask import Flask, render_template, Response, request ,jsonify
import json
import couchdb
import json
import requests

app = Flask(__name__)

xdays = ["shirts", "cardigan", "sneaker", "pants", "highheel", "sock"]
yvalues = [5, 20, 36, 10, 10, 20]
json_data = json.dumps({"xdays": xdays, "yvalues": yvalues})

@app.route("/viewdata", methods=["POST"])
def viewdata():
    if request.method == "POST":
        return json_data
    else:
        return json_data

@app.route('/view_city', methods = ['GET', 'POST'])
def get_view():
    return map_reduce_fuc()

@app.route('/')
def hello():
    return render_template('my_template.html')
    
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

if __name__ == "__main__":
    app.run(debug=True,port=5000)