__author__ = 'kfranko'


#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API
consumer_key = 'WxrPOgQJRLt2RdLKNakXqZl2T'
consumer_secret = '7SR9t3xMKTtLx1JaAVgqLvCE627TA5x81juQZoww2w5mydDbL9'
access_token = '3168994794-JhNYLog1BLt2XWcM8Z94V0KCeQNi5Dw2VlzbadP'
access_secret = 'C4pLGZyr7tUgYroVmSpLtit4mDYKfOkDr4mk7ibcoi2BU'


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        try:
            with open('beer_coffee.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'coffee' or 'beer'
    stream.filter(track=['coffee', 'beer'])
