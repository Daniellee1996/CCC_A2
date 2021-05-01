import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

CONSUMER_KEY = "ZRe0EbBzCbWYvo8fcI7R2Cmah"
CONSUMER_SECRET = "JpofwKllwrSUjISwuvihaFu1Lb4iUWlTlwGssPEUqswT4woyhf"
ACCESS_TOKEN = "1131912292054863872-An1go1FZ4dRRAopydTKVoNhEM1THW9"
ACCESS_SECRET = "fvarVeChN9jBHqdMbeD42yBs1XHUUGI9KK5ctRBoxGDg6"


GEOBOX_VIC = [143.997737216,-37.3844385432, 146.0421447046,-38.1044516321]
GEOBOX_MELB = [143.997737216,-37.3844385432, 146.0421447046,-38.1044516321]
GEOBOX_AU = [112.8206091857,-44.1201660185,153.8847571349,-10.1940259781]
class StdOutListener(StreamListener):
    """
    This is a basic listener class that just prints received tweets to stdout.
    """

    def on_data(self, data):
        try:
            with open("stream_sample.json", 'a') as tf:
                tf.write(data)
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


#hash_tag_list = ["vegan", "vegetarian", "veggie", 'vegie', 'veganism', 'plant-eating', 'plant-based', 'vegetarianism']
listener = StdOutListener()
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
stream = Stream(auth, listener)
#stream.filter(track=hash_tag_list,locations = GEOBOX_MELB)
stream.filter(track=["covid"])




# import tweepy

# stream = tweepy.Stream(
#   CONSUMER_KEY, CONSUMER_SECRET,
#   ACCESS_TOKEN, ACCESS_SECRET
# )
# stream.filter(track=["covid"])
