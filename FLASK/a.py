from flask import Flask, render_template, Response, request ,jsonify
import json
import couchdb
import json
import requests
from Backend import socio_enconomic_covid
from Twitter_Harvester import couchDB_setting
app = Flask(__name__)

twitter_count = {"total": 0, "Adelaide": 0, "Melbourne": 0, "Mornington": 0, "Perth": 0, "Sydney": 0}

@app.route('/')
def hello():
    return render_template('test.html')
    

@app.route('/view_city', methods = ['GET', 'POST'])
def get_view():
    return couchDB_setting.reduce_covid_time()
    #return socio_enconomic_covid.covid_relate_income()

@app.route('/refresh_count')
def refresh_count():
	global twitter_count
	return jsonify(
		Total = twitter_count["total"],
		Adelaide = twitter_count["Adelaide"],
		Melbourne = twitter_count["Melbourne"],
		Morningtom = twitter_count["Mornington"],
        Perth = twitter_count["Perth"],
        Sydney = twitter_count["Sydney"])

if __name__ == "__main__":
    app.run(debug=True,port=5000)
