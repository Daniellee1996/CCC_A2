import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import argparse
import time
import csv
import json
import simplejson
import pandas as pd
import couchdb
import json
import os
from pathlib import Path
#from config import TwitterCredentails # your keys, format list of dicts
from couchDB_setting import *
from sentimental_score_calculator import SentiScoreCalculator

KEY_INDEX = 0
ID_INDEX = 0
N_IDS = 0
TwitterCredentails = [
    # shuyu li
    {
        'API_KEY':'ZRe0EbBzCbWYvo8fcI7R2Cmah',
        'API_SECRET_KEY':'JpofwKllwrSUjISwuvihaFu1Lb4iUWlTlwGssPEUqswT4woyhf',
        'ACCESS_TOKEN': '1131912292054863872-An1go1FZ4dRRAopydTKVoNhEM1THW9',
        'ACCESS_TOEKN_SECRET':'fvarVeChN9jBHqdMbeD42yBs1XHUUGI9KK5ctRBoxGDg6',
        'BEARER_TOKEN':'AAAAAAAAAAAAAAAAAAAAAAK9OwEAAAAA%2FgK%2ByLXx%2FQXcmcA9YVl4z3Bdx1w%3D8Xu5hQ2gLyqNOemnbVV5s2PoDFdnZvQhRTtd0XFXk2iCxPMcJl'
    },
    # kd
    {
        'API_KEY':'aY9489Yex1OjIOaLrAZ0fDils',
        'API_SECRET_KEY':'4iogUNgX71wcz9l85Z4BNaW4cLg8xpdNcuosQjrUkvtF2tq5aE',
        'ACCESS_TOKEN': '1289252085033127936-ptoDhOwwYThSPW6qgQuihhV2NI8EWA',
        'ACCESS_TOEKN_SECRET':'0DwAasvL9Ob9VX4iZg681AZCD07bq1N7e7ZehTfqJS0mI',
        'BEARER_TOKEN':'AAAAAAAAAAAAAAAAAAAAAEJaPAEAAAAA37Fvd1A5M8pU7%2FfTFB2kbxRRpzY%3DYjvYAB0XIGQDk8J5oF2GvkNavfwFgyYSdnCasjocDa46HWym3u'
    }
]
#CouchDB authentication
COUCHDB_SERVER='http://admin:admin@172.26.128.214:5984/'
DBNAME = 'test'
couch = couchdb.Server(COUCHDB_SERVER)
db = couch[DBNAME]

#Access tokens

def load_api():
    ''' Function that loads the twitter API after authorizing the user. '''
    """ todo: switch keys when window limit is reached """
    consumer_key = TwitterCredentails[KEY_INDEX].get('API_KEY')
    consumer_secret = TwitterCredentails[KEY_INDEX].get('API_SECRET_KEY')
    access_token = TwitterCredentails[KEY_INDEX].get('ACCESS_TOKEN')
    access_secret = TwitterCredentails[KEY_INDEX].get('ACCESS_TOEKN_SECRET')
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    # load the twitter API via tweepy
    return tweepy.API(auth)

def switch_keys():
    max_index = len(TwitterCredentails) - 1
    global KEY_INDEX
    if KEY_INDEX == max_index:
        KEY_INDEX = 0
    else:
        KEY_INDEX += 1

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

def get_tweeet_using_id(user_id, api):
    alltweets = []
    new_tweets = api.user_timeline(user_id = user_id, count=200)
    alltweets.extend(new_tweets)
    # save the id of the oldest tweet less one to avoid duplication
    oldest = alltweets[-1].id - 1
    # keep grabbing tweets until there are no tweets left
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))
    # all subsequent requests use the max_id param to prevent
    # duplicates
        new_tweets = api.user_timeline(user_id = user_id, count=200, max_id=oldest)
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
    return alltweets

def tweet_upload(alltweets):
    for tweet in alltweets:
        _json = tweet._json
        c = SentiScoreCalculator(_json)
        _json['polarity'] = c.get_polarity()
        _json['subjectivity'] = c.get_subjectivity()
        upload2couchDB(_json)

def tweet_write(alltweets, outfile = 'user_timeline_sample.txt'):
    with open(outfile, 'a') as f:
        for tweet in alltweets:
            _json = tweet._json
            c = SentiScoreCalculator(_json)
            _json['polarity'] = c.get_polarity()
            _json['subjectivity'] = c.get_subjectivity()
            json.dump(tweet._json, f)
    

def main():
    global N_IDS, ID_INDEX
    api = load_api()
    ids = list(pd.read_csv('id_excl_dups.csv', index_col= False)['id'])
    ids = ids[ID_INDEX:]
    N_IDS = len(ids)
    print('havesting started')
    for i in range(N_IDS):
        uid = ids[i]
        try:
            tweets = get_tweeet_using_id(uid, api)
            tweet_upload(tweets)
            # tweet_write(tweets)
        except tweepy.TweepError as e:
            if e.api_code == 34: # no id matched
               continue
            elif e.api_code == 88: # limit rate
                ID_INDEX += i
                switch_keys()
                main()
            else:
                print('found other error')
                print(e)
                ID_INDEX += i
                switch_keys()
                main()






    



if __name__ == '__main__':
    # api = load_api()
    # screen_names = []
    # with open('stream_sample.txt') as f:
    #     for line in f:
    #         screen_names.append(json.loads(line)['user']['screen_name'])
	# #pass in the username of the account you want to download
    # print('havesting started')
    # for n in screen_names:
	#     get_all_tweets(n)
    # print('done')
    main()
    