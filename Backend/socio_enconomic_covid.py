from Twitter_Harvester import couchDB_setting
from Backend import lga_city






def covid_relate_enconomic():
    city_enco_index = lga_city.city_socio_enconomic(lga_city.generate_lga_city())
    covid_city_tweet = couchDB_setting.reduce_covid()
    covid_city_index = {}
    for city,value in covid_city_tweet.items():
        city = city.split(",")[0]

        if city in city_enco_index:
            if city not in covid_city_index:
                covid_city_index[city] = [value,city_enco_index[city]]
            else:
                covid_city_index[city][0]+=value
    # for key,value in covid_city_index.items():
    #     print(key,value)
    return covid_city_index

def covid_relate_income():
    city_enco_index = lga_city.city_median(lga_city.generate_lga_city())
    covid_city_tweet = couchDB_setting.reduce_covid()
    covid_city_index = {}
    for city, value in covid_city_tweet.items():
        city = city.split(",")
        #print(city)
        for c in city:
            if c in city_enco_index:
                if c not in covid_city_index:
                    covid_city_index[c] = [value, city_enco_index[c]]
                else:
                    covid_city_index[c][0] += value


    # for key, value in covid_city_index.items():
    #     print(key, value)
    return covid_city_index


# covid_relate_enconomic()
# print("=========================")
# covid_relate_income()
#couchDB_setting.reduce_city_num()