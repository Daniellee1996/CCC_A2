from Twitter_Harvester import couchDB_setting
from Socio_enconomic import lga_city






def covid_relate_enconomic():
    city_enco_index = lga_city.city_socio_enconomic(lga_city.generate_lga_city())
    covid_city_tweet = couchDB_setting.reduce_covid()
    for city,value in covid_city_tweet.items():
        if city in city_enco_index:
            print(city,city_enco_index[city],value)


