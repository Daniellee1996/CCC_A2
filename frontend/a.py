from flask import Flask, render_template, Response, request ,jsonify
import json
import couchdb
import json
import requests
from Backend import socio_enconomic_covid as sc
app = Flask(__name__)

twitter_count = {"total": 0, "Adelaide": 0, "Melbourne": 0, "Mornington": 0, "Perth": 0, "Sydney": 0}



@app.route('/index')
def homepage():
    return render_template('index.html')
    
COUCHDB_SERVER='http://admin:admin@172.26.128.214:5984/'
DBNAME = 'twitter'
couch = couchdb.Server(COUCHDB_SERVER)
db = couch[DBNAME]


@app.route('/simple_page')
def simple_page():
    return render_template('simple_page.html')

@app.route('/shortcodes')
def shortcodes():
    return sc.covid_relate_income()

@app.route('/view_city', methods = ['GET', 'POST'])
def get_view():
    list_covid_time = {}
    for item in db.view('covid_time/filter_covid_time', group_level='2', reduce='true'):
        date = item.key.split("-")
        print(date)
        time = date[0] + "-" + date[1]
        if time not in list_covid_time:
            list_covid_time[time] = item.value
        else:
            list_covid_time[time] += item.value
    # print(list_covid_time)
    return list_covid_time

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