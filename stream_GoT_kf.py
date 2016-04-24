'''
streaming for first episode
april 24 2016
emily
'''

import yaml
import os
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
import datetime


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

    # try streaming based on GoT search terms
    print '\rscript start time is:', datetime.datetime.now()
    time_start = datetime.datetime.now().time()
    stream.filter(track=['gameofthrones', 'game of thrones'])

# (note: do we maybe want to only collect certain fields to cut down on file size? for example:
#     def on_status(self, status):
#        text = status.text
#        created = status.created_at
#        record = {'Text': text, 'Created At': created}
#        print record #See Tweepy documentation to learn how to access other fields
#        collection.insert(record)

# from: http://stackoverflow.com/questions/20863486/tweepy-streaming-stop-collecting-tweets-at-x-amount)