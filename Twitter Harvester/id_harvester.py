import tweepy
from tweepy import OAuthHandler
import pandas as pd
import datetime
import time
from config import TwitterCredentails # your keys, format list of dicts

KEY_INDEX = 0
MAX_ID = None
N_IDS = 0
TIME = [None, None, None]


def load_api():
    ''' Function that loads the twitter API after authorizing the user. '''
    """ todo: switch keys when window limit is reached """
    global KEY_INDEX, TIME
    consumer_key = TwitterCredentails[KEY_INDEX].get('API_KEY')
    consumer_secret = TwitterCredentails[KEY_INDEX].get('API_SECRET_KEY')
    access_token = TwitterCredentails[KEY_INDEX].get('ACCESS_TOKEN')
    access_secret = TwitterCredentails[KEY_INDEX].get('ACCESS_TOEKN_SECRET')
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    # load the twitter API via tweepy
    TIME[KEY_INDEX] = time.time()
    return tweepy.API(auth)


def switch_keys():
    max_index = len(TwitterCredentails) - 1
    global KEY_INDEX
    if KEY_INDEX == max_index:
        KEY_INDEX = 0
    else:
        KEY_INDEX += 1

def get_AU_place_id(api):
    place = api.geo_search(query="AU", granularity = "country")
    return place[0].id

def tweet_write(user_id, outfile = 'cursor_ids.txt'):
    with open(outfile, 'a') as f:
        f.write(user_id + '\n')

def main():
    global KEY_INDEX, MAX_ID, N_IDS, TIME
    api = load_api()
    # api.verify_credentials()
    AU_place_id = get_AU_place_id(api)
    print('harvesting started')
    while True:
        try:
            new_tweets = tweepy.Cursor(api.search, 
                                        q="place:%s"%AU_place_id, 
                                        until=datetime.datetime.today().strftime("%Y-%m-%d"),
                                        lang="en", 
                                        tweet_mode="extended", 
                                        max_id = MAX_ID).items(100)

            id_uids = [[tweet.id, tweet.user.id_str] for tweet in new_tweets]

            for id, uid in id_uids:
                tweet_write(uid)

            MAX_ID = id_uids[-1][0] - 1
            N_IDS += len(id_uids)
            print(N_IDS, 'ids harvested...')

        except tweepy.error.TweepError as e:
            if None in TIME:
                print(e)
                switch_keys()
                print('key switched to', KEY_INDEX)
                main()
            elif time.time() - min(TIME) < 60 * 15:
                time.sleep(15 * 60 - (time.time() - min(TIME)) + 10)
                print(e)
                switch_keys()
                print('key switched to', KEY_INDEX)
                main()
            else:
                print(e)
                switch_keys()
                print('key switched to', KEY_INDEX)
                main()
                
        except StopIteration:
            print(new_tweets)
            pass
        
if __name__ == '__main__':
    main()