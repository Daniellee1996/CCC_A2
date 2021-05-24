from flask import Flask, render_template, Response, request ,jsonify
import json
import couchdb
import json
import requests
from Backend import socio_enconomic_covid as sc
app = Flask(__name__)
from Twitter_Harvester import couchDB_setting

twitter_count = {"total": 0, "Adelaide": 0, "Melbourne": 0, "Mornington": 0, "Perth": 0, "Sydney": 0}



@app.route('/index')
def homepage():
    return render_template('index.html')
    
# COUCHDB_SERVER='http://admin:admin@172.26.128.214:5984/'
# DBNAME = 'twitter'
# couch = couchdb.Server(COUCHDB_SERVER)
# db = couch[DBNAME]


@app.route('/simple_page')
def simple_page():
    return render_template('simple_page.html')

@app.route('/trend')
def trend():
    return render_template('trend.html')

@app.route('/view_trend', methods = ['GET', 'POST'])
def get_view():
    list_covid_time = couchDB_setting.reduce_covid_time()

    date = []
    num_tweet = []
    j_dict = {}
    for key,value in list_covid_time.items():
        date.append(key)
        num_tweet.append(value)
    j_dict['key'] = date
    j_dict['value'] = num_tweet
    j = json.dumps(j_dict)
    return j

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
