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

@app.route('/view_total', methods = ['GET', 'POST'])
def view_total():   
    data = [{"name": "Adelaide", "value": 364}, {"name": "Brisbane", "value": 606}, {"name": "Bunbury", "value": 1}, {"name": "Cairns", "value": 1}, {"name": "Central Coast", "value": 1}, {"name": "Cottesloe", "value": 1}, {"name": "Fremantle", "value": 1}, {"name": "Gawler", "value": 2}, {"name": "Gold Coast", "value": 721}, {"name": "Hobart", "value": 1}, {"name": "Kempsey", "value": 1}, {"name": "Melbourne", "value": 1705}, {"name": "Newcastle", "value": 4}, {"name": "Perth", "value": 314}, {"name": "Rockhampton", "value": 2}, {"name": "Sunshine Coast", "value": 62}, {"name": "Sydney", "value": 959}, {"name": "Townsville", "value": 7}, {"name": "Victor Harbor", "value": 107}, {"name": "Wollondilly", "value": 129}, {"name": "Wollongong", "value": 1}]
    j = {"key": data}
    return json.dumps(j)

@app.route('/total')
def total():
    return render_template('total.html')

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

@app.route('/trend')
def trend():
    return render_template('trend.html')

@app.route('/view_income')
def income():
    income_covid = sc.covid_relate_income()
    city_name = []
    city_covid_income = []
    city_covid_num = []
    j_dict = {}
    for key, value in income_covid.items():
        city_name.append(key)
        city_covid_num.append(value[0])
        city_covid_income.append(value[1])
    j_dict['key'] = city_name
    j_dict['income'] = city_covid_income
    j_dict['num'] =city_covid_num
    j = json.dumps(j_dict)
    return j

@app.route('/income')
def simple_page():
    return render_template('income.html')

@app.route('/view_city_economic')
def enconomic():
    sc_covid = sc.covid_relate_enconomic()
    city_name = []
    city_covid_enconomic = []
    city_covid_num = []
    j_dict = {}
    for key, value in sc_covid.items():
        city_name.append(key)
        city_covid_num.append(value[0])
        city_covid_enconomic.append(value[1])
    j_dict['key'] = city_name
    j_dict['economic'] = city_covid_enconomic
    j_dict['num'] = city_covid_num
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
