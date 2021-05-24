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

@app.route('/view_income')
def income():
    income_covid = sc.covid_relate_income()
    city_name = []
    city_covid_income = []
    j_dict = {}
    for key, value in income_covid.items():
        city_name.append(key)
        city_covid_income.append(value)
    j_dict['key'] = city_name
    j_dict['value'] = city_covid_income
    j = json.dumps(j_dict)
    return j

@app.route('/view_city_enconomic')
def enconomic():
    sc_covid = sc.covid_relate_enconomic()
    city_name = []
    city_covid_enconomic = []
    j_dict = {}
    for key, value in sc_covid.items():
        city_name.append(key)
        city_covid_enconomic.append(value)
    j_dict['key'] = city_name
    j_dict['value'] = city_covid_enconomic
    j = json.dumps(j_dict)
    return j



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
