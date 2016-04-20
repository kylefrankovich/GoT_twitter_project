'''

test run twitter streaming
april 19 2016
emily

'''


'''
tutorial: http://adilmoujahid.com/posts/2014/07/twitter-analytics/

'''

# loading secrets into workspace for sake of practice
# in actual script will need to add this by reading in secret.yaml and accessing dictionary


# use tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream


#This is a basic listener that just prints received tweets to stdout.


class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript', 'ruby'])