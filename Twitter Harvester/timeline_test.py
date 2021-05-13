import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import argparse
import json as js
import time
import csv
import json
import pandas as pd
import couchdb
import json
import os
from pathlib import Path
from config import TwitterCredentails # your keys, format list of dicts
from couchDB_setting import *
from sentimental_score_calculator import SentiScoreCalculator


#CouchDB authentication
# COUCHDB_SERVER='http://admin:password@172.26.132.199:5984/'
# DBNAME = 'test'
# couch = couchdb.Server(COUCHDB_SERVER)
# db = couch[DBNAME]

#Access tokens

def load_api():
    ''' Function that loads the twitter API after authorizing the user. '''
    """ todo: switch keys when window limit is reached """
    consumer_key = TwitterCredentails[0].get('API_KEY')
    consumer_secret = TwitterCredentails[0].get('API_SECRET_KEY')
    access_token = TwitterCredentails[0].get('ACCESS_TOKEN')
    access_secret = TwitterCredentails[0].get('ACCESS_TOEKN_SECRET')
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    # load the twitter API via tweepy
    return tweepy.API(auth)

def get_all_tweets(screen_name):
    alltweets = []
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    alltweets.extend(new_tweets)
    # save the id of the oldest tweet less one to avoid duplication
    oldest = alltweets[-1].id - 1
    # keep grabbing tweets until there are no tweets left
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))
    # all subsequent requests use the max_id param to prevent
    # duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
    # save most recent tweets
        alltweets.extend(new_tweets)
    # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        print("...%s tweets downloaded so far" % (len(alltweets)))
    ### END OF WHILE LOOP ###
    #for t in alltweets:
        #print(t)
    # outtweets = [[tweet.id, tweet.created_at, tweet.place, tweet.coordinates, tweet.text, tweet.entities, tweet.retweet_count, tweet.favorite_count,
    # tweet.lang, tweet.user] for tweet in alltweets]
    # print(outtweets)

    for tweet in alltweets:
        _json = tweet._json
        c = SentiScoreCalculator(_json)
        _json['polarity'] = c.get_polarity()
        _json['subjectivity'] = c.get_subjectivity()
        upload2couchDB(_json)

    # with open('screen_name.csv', 'a') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["id", "created_at", "place", "coordinates", "text", 
    #     "entities", "retweet_count", "favorite_count", "lang", "user"])
    #     writer.writerows(outtweets)
    # pass
    # for tweet in outtweets:
    #     data = {}
    #     data['id'] = tweet[0]
    #     data['created_at'] = str(tweet[1])
    #     print(type(tweet[1]))
    #     data['place'] = str([tweet[2]])
    #     print(type(tweet[2]))
    #     data['coordinates'] = str(tweet[3])
    #     data['text'] = str(tweet[4])
    #     data['entities'] = str(tweet[5])
    #     data['retweet_count'] = str(tweet[6])
    #     data['favorite_count'] = str(tweet[7])
    #     data['lang'] = tweet[8]
    #     data['user'] = str(tweet[9])
    #     print(type(tweet[9]))
    #     print('')
    #     # jsonFile = json.dumps(data)
    #     # db.save(data)
    # pass



if __name__ == '__main__':
    api = load_api()
    screen_names = []
    with open('stream_sample.txt') as f:
        for line in f:
            screen_names.append(js.loads(line)['user']['screen_name'])
	#pass in the username of the account you want to download
    for n in screen_names:
	    get_all_tweets(n)
    print('done')