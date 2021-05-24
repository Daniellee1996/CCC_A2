from flask import Flask, render_template, Response, request ,jsonify
import json
import couchdb
import json
import requests
from Backend import socio_enconomic_covid as sc
from Backend import city_polarity_subjectivity as ps
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

@app.route('/income')
def income_page():
    return render_template('income.html')

@app.route('/polarity')
def get_polarity():
    polarity = ps.get_city_polarity()
    city_name = []
    city_polarity = []
    j_dict = {}
    for c,p in polarity.items():
        city_name.append(c)
        city_polarity.append(p)
    j_dict['city'] = city_name
    j_dict['polarity'] = city_polarity
    j = json.dumps(j_dict)

    return j

@app.route('/subjectivity')
def get_subjectivity():
    polarity = ps.get_city_subjectivity()
    city_name = []
    city_sub = []
    j_dict = {}
    for c,s in polarity.items():
        city_name.append(c)
        city_sub.append(s)
    j_dict['city'] = city_name
    j_dict['subjectivity'] = city_sub
    j = json.dumps(j_dict)

    return j



@app.route('/view_covid_city')
def covid_city():
    income_covid = sc.covid_relate_income()
    covid_city_dicts = []

    for key,value in income_covid.items():
        j_dict = {}
        j_dict['name'] = key
        j_dict['value'] = value[0]
        covid_city_dicts.append(j_dict)
    j = json.dumps(covid_city_dicts)



    return j



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
