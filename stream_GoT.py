'''
streaming for first episode
april 24 2016
emily
'''

import yaml
import os
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream

os.chdir('./GoT_twitter_project')

f = open('secrets.yaml')
secret_dict = yaml.safe_load(f)


class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    # This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(secret_dict['consumer_key'], secret_dict['consumer_secret'])
    auth.set_access_token(secret_dict['access_token'], secret_dict['access_token_secret'])
    stream = Stream(auth, l)

    # try streaming based on democratic primary
    stream.filter(track=['gameofthrones', 'game of thrones'])