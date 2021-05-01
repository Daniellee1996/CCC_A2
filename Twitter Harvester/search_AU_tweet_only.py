#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on April 23 10:32:28 2020

@author: danny
"""
import tweepy
from tweepy import OAuthHandler
import datetime as dt
import time
import json
from config import TwitterCredentails # your keys, format list of dicts


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

def tweet_search(api, query, max_tweets, max_id, geocode):
    ''' Function that takes in a search string 'query', the maximum
        number of tweets 'max_tweets', and the minimum (i.e., starting)
        tweet id. It returns a list of tweepy.models.Status objects. '''

    searched_tweets = []
    while len(searched_tweets) < max_tweets:
        remaining_tweets = max_tweets - len(searched_tweets)
        try:
            new_tweets = api.search(q=query, count=remaining_tweets, max_id=max_id, geocode=geocode)
            print('found',len(new_tweets),'tweets')
            if not new_tweets:
                print('no tweets found')
                break
            searched_tweets.extend(new_tweets)
        except tweepy.TweepError:
            print('exception raised, waiting 16 minutes')
            print('(until:', dt.datetime.now()+dt.timedelta(minutes=16), ')')
            time.sleep(16*60)
            break # stop the loop
    return searched_tweets

def main():
    latest_max_id = []
    search_list = ['vegan OR #vegan', 'veggie OR #veggie', 'vegie OR #vegie', 'vegetarian OR #vegetarian',
                   'veganism OR #veganism', 'plant-eating OR #plant-eating', 'herbivorous OR #herbivorous', 
                   'plant-based OR #plant-based', 'vegetarianism OR #vegetarianism']
#    search_list = ['covid OR #covid']
    geocode="-23.8136,133.9631,2500km"
    time_limit = 9 # time limit in hours
    start = dt.datetime.now()
    end = start + dt.timedelta(hours=time_limit)
    api = load_api()
    iteration = 0
    print('harvesting started')
    for q in search_list:
        new_tweets = api.search(q=q, geocode=geocode)
        maxid = new_tweets[0]._json.get('id')
        latest_max_id.append(maxid)
    with open('search_sample.json', 'a') as f:    
        for query, mid in zip(search_list,latest_max_id):
            maxid = mid
            while dt.datetime.now() < end:
                try:
                    iteration += 1    
                    new_tweets = api.search(q=query, geocode=geocode, max_id = maxid)
                    if not new_tweets:
                        print('no tweets found')
                        break
                    new_maxid = new_tweets[-1]._json.get('id')
                    if new_maxid == maxid:
                        break;
                    else:
                        maxid = new_maxid - 1
                    for tweet in new_tweets:                   
                        json.dump(tweet._json, f)
                        f.write('\n')
                except tweepy.TweepError:
                    print('exception raised, waiting 16 minutes')
                    print('(until:', dt.datetime.now()+dt.timedelta(minutes=16), ')')
                    time.sleep(16*60)

if __name__ == "__main__":
    main()