import json

from Twitter_Harvester import couchDB_setting
from Backend import lga_city



#get the polarity of city
def get_city_polarity():

    p = couchDB_setting.reduce_polarity()
    c = couchDB_setting.reduce_city_num()
    v = couchDB_setting.reduce_covid()
    lga = lga_city.generate_lga_city()
    city_enco_index = lga_city.city_median(lga)
    covid_city_polarity = {}
    covid_city_num = {}
    for city,value in v.items():
        city_list = city.split(",")
        # print(city)
        for ct in city_list:
            if ct in city_enco_index:
                if ct not in covid_city_polarity:
                    covid_city_polarity[ct] = p[city]
                else:
                    covid_city_polarity[ct] += p[city]

    for city,value in v.items():
        city_list = city.split(",")
        for ct in city_list:
            if ct in city_enco_index:
                if ct not in covid_city_num:
                    covid_city_num[ct] = c[city]
                else:
                    covid_city_num[ct] += c[city]


    for city,polarity in covid_city_polarity.items():
        covid_city_polarity[city] = polarity/covid_city_num[city]
    print(covid_city_polarity)
    return covid_city_polarity

def get_city_subjectivity():
    p = couchDB_setting.reduce_subjectivity()
    c = couchDB_setting.reduce_city_num()
    lga = lga_city.generate_lga_city()
    v = couchDB_setting.reduce_covid()
    city_enco_index = lga_city.city_median(lga)
    covid_city_polarity = {}
    covid_city_num = {}
    for city,value in v.items():
        city_list = city.split(",")
        # print(city)
        for ct in city_list:
            if ct in city_enco_index:
                if ct not in covid_city_polarity:
                    covid_city_polarity[ct] = p[city]
                else:
                    covid_city_polarity[ct] += p[city]

    for city,value in v.items():
        city_list = city.split(",")
        for ct in city_list:
            if ct in city_enco_index:
                if ct not in covid_city_num:
                    covid_city_num[ct] = c[city]
                else:
                    covid_city_num[ct] += int(value)


    for city,polarity in covid_city_polarity.items():
        covid_city_polarity[city] = polarity/covid_city_num[city]
    #print(covid_city_polarity)
    return covid_city_polarity

def get_sub_pol():
    p = couchDB_setting.reduce_polarity()
    s = couchDB_setting.reduce_subjectivity()
    c = couchDB_setting.reduce_city_num()
    v = couchDB_setting.reduce_covid()
    lga = lga_city.generate_lga_city()
    city_enco_index = lga_city.city_median(lga)
    #get the number of covid twitter city
    covid_city_num = {}
    for city,value in v.items():
        city_list = city.split(",")
        for ct in city_list:
            if ct in city_enco_index:
                if ct not in covid_city_num:
                    covid_city_num[ct] = c[city]
                else:
                    covid_city_num[ct] += int(value)

    covid_city_polarity = {}
    for city,value in v.items():
        city_list = city.split(",")
        # print(city)
        for ct in city_list:
            if ct in city_enco_index:
                if ct not in covid_city_polarity:
                    covid_city_polarity[ct] = p[city]
                else:
                    covid_city_polarity[ct] += p[city]

    covid_city_subjectivity = {}
    for city,value in v.items():
        city_list = city.split(",")
        # print(city)
        for ct in city_list:
            if ct in city_enco_index:
                if ct not in covid_city_subjectivity:
                    covid_city_subjectivity[ct] = s[city]
                else:
                    covid_city_subjectivity[ct] += s[city]


    j_dict = {}
    city_names = []
    subjectivity = []
    polarity = []

    for key,value in covid_city_num.items():
        city_names.append(key)
        subjectivity.append(covid_city_subjectivity[key]/value)
        polarity.append(covid_city_polarity[key]/value)

    j_dict['key'] = city_names
    j_dict['subjectivity'] = subjectivity
    j_dict['polarity'] = polarity
    print(j_dict)
    return json.dumps(j_dict)


