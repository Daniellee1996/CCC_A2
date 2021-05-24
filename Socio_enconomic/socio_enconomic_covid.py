from Twitter_Harvester import couchDB_setting
from Socio_enconomic import lga_city






def covid_relate_enconomic():
    city_enco_index = lga_city.city_socio_enconomic(lga_city.generate_lga_city())
    covid_city_tweet = couchDB_setting.reduce_covid()
    covid_city_index = {}
    for city,value in covid_city_tweet.items():
        city = city.split(",")[0]
        print(city)
        if city in city_enco_index:
            if city not in covid_city_index:
                covid_city_index[city] = [value,city_enco_index[city]]
            else:
                covid_city_index[city][0]+=value
    for key,value in covid_city_index.items():
        print(key,value)
    return city_enco_index

def covid_relate_income():
    city_enco_index = lga_city.city_median(lga_city.generate_lga_city())
    covid_city_tweet = couchDB_setting.reduce_covid()
    covid_city_index = {}
    for city, value in covid_city_tweet.items():
        city = city.split(",")[0]
        print(city)
        if city in city_enco_index:
            if city not in covid_city_index:
                covid_city_index[city] = [value, city_enco_index[city]]
            else:
                covid_city_index[city][0] += value
    for key, value in covid_city_index.items():
        print(key, value)
    return city_enco_index


