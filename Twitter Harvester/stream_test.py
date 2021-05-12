import tweepy
import datetime as dt
import logging
import couchdb
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from config import TwitterCredentails # your keys, format list of dicts
from urllib3.exceptions import ProtocolError
import time

GEOBOX_VIC = [143.997737216,-37.3844385432, 146.0421447046,-38.1044516321]
GEOBOX_MELB = [143.997737216,-37.3844385432, 146.0421447046,-38.1044516321]
GEOBOX_AU = [112.8206091857,-44.1201660185,153.8847571349,-10.1940259781]
MAX_TWEETS = 50000
N_HARVESTED = 0
KEY_INDEX = 0

# couchDB set up
COUCHDB_SERVER='http://admin:admin@172.26.132.158:49186/'
DBNAME = 'stream_test'
couch = couchdb.Server(COUCHDB_SERVER)
db = couch[DBNAME]

logging.basicConfig(filename='stream.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

def upload2couchDB(row):
    data = json.loads(row)
    db.save(data)

def switch_keys():
    max_index = len(TwitterCredentails) - 1
    global KEY_INDEX
    if KEY_INDEX == max_index:
        KEY_INDEX = 0
    else:
        KEY_INDEX += 1

def load_auth(index = KEY_INDEX):
    ''' Function that loads the twitter API after authorizing the user. '''
    """ todo: switch keys when window limit is reached """
    consumer_key = TwitterCredentails[index].get('API_KEY')
    consumer_secret = TwitterCredentails[index].get('API_SECRET_KEY')
    access_token = TwitterCredentails[index].get('ACCESS_TOKEN')
    access_secret = TwitterCredentails[index].get('ACCESS_TOEKN_SECRET')
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    # load the twitter API via tweepy
    return auth

def write2file(data):
    with open("stream_sample.txt", 'a') as tf:
        tf.write(data)
        global N_HARVESTED
        N_HARVESTED += 1
        if N_HARVESTED % 10 == 0:
            print(N_HARVESTED, 'tweets havested')

class StdOutListener(StreamListener):
    """
    This is a basic listener class that just prints received tweets to stdout.
    """

    def on_data(self, data):
        try:
            write2file(data)
            # upload2couchDB(data)
            global N_HARVESTED
            N_HARVESTED += 1
            if N_HARVESTED % 10 == 0:
                print(N_HARVESTED, 'tweets havested')
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False
        elif status_code == 401:
            print('keys corrected')
            return False


#hash_tag_list = ["vegan", "vegetarian", "veggie", 'vegie', 'veganism', 'plant-eating', 'plant-based', 'vegetarianism']
# listener = StdOutListener()
# auth = load_auth()
# stream = Stream(auth, listener)
# #stream.filter(track=hash_tag_list,locations = GEOBOX_MELB)
# stream.filter(track=["covid"])
# print(stream.running)
def srteam_havest(max_tweets = MAX_TWEETS, track = ["covid"], locations = GEOBOX_MELB): # typo
    global N_HARVESTED
    logging.debug('harvesting started with max tweets = %s', MAX_TWEETS)
    while N_HARVESTED <= max_tweets:
        try:
            listener = StdOutListener()
            auth = load_auth()
            stream = Stream(auth, listener)
            stream.filter(track = track, locations = locations)
            if stream.running == False:
                print('switching keys from %s', KEY_INDEX)
                logging.debug('switching keys from %s', KEY_INDEX)
                switch_keys()
                auth = load_auth()
                logging.debug('switching keys to %s', KEY_INDEX)
                print('switching keys to %s', KEY_INDEX)
                stream = Stream(auth, listener)
                stream.filter(track = track, locations = locations)
        except tweepy.TweepError as e:
            print('exception raised, waiting 16 minutes')
            print(e)
            print('(until:', dt.datetime.now()+dt.timedelta(minutes=16), ')')
            time.sleep(16*60)
        except Exception as e:
            print(e)
            time.sleep(60)
            srteam_havest(max_tweets,track,locations)



if __name__ == '__main__':
    srteam_havest(track = None, locations = GEOBOX_AU)