from flask import Flask, render_template, Response, request ,jsonify
import json
import couchdb
import json
import requests
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
sys.path.append(BASE_DIR)
print(BASE_DIR)
sys.path.append('../Backend')
from Backend import socio_enconomic_covid as sc
from Backend import city_polarity_subjectivity as ps
from Twitter_Harvester import couchDB_setting

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')
    
# COUCHDB_SERVER='http://admin:admin@172.26.128.214:5984/'
# DBNAME = 'twitter'
# couch = couchdb.Server(COUCHDB_SERVER)
# db = couch[DBNAME]

@app.route('/view_total', methods = ['GET', 'POST'])
def view_total():
    income_covid = sc.covid_relate_income()
    covid_city_dicts = []

    for key, value in income_covid.items():
        j_dict = {}
        j_dict['name'] = key
        j_dict['value'] = value[0]
        covid_city_dicts.append(j_dict)
    j = {"key": covid_city_dicts}
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
    sc_covid = sc.covid_relate_enconomic()
    income_covid = sc.covid_relate_income()
    print("get_income")
    city_name = []
    city_covid_income = []
    city_covid_num = []
    city_covid_enconomic = []
    j_dict = {}
    for value in sc_covid.values():
        city_covid_enconomic.append(value[1])


    for key, value in income_covid.items():
        city_name.append(key)
        city_covid_num.append(value[0])
        city_covid_income.append(value[1])
    j_dict['key'] = city_name
    j_dict['income'] = city_covid_income
    j_dict['num'] =city_covid_num
    j_dict['economic'] = city_covid_enconomic

    j = json.dumps(j_dict)
    print("get_income11")
    return j

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

@app.route('/subjectivity_polarity')
def get_subjectivityAndPolarity():
    return ps.get_sub_pol()



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

@app.route('/view_relation', methods = ['GET', 'POST'])
def view_relation():
    ec_covid = sc.covid_relate_enconomic()
    income_covid = sc.covid_relate_income()
    print("get_relation")
    city_covid_enconomic = []
    city_covid_income = []

    j_dict = {}
    for key,value in ec_covid.items():

        city_covid_enconomic.append([value[0],value[1]])

    for key,value in income_covid.items():
        city_covid_income.append([value[0],value[1]])

    j_dict['income'] = sorted(city_covid_income)
    j_dict['economic'] = sorted(city_covid_enconomic)
    j = json.dumps(j_dict)
    print("get_relation11")
    return j



if __name__ == "__main__":
    app.run(debug=True,port=5000)
