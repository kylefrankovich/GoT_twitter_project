'''
initial attempt to
 - read in data streamed from twitter after NY primary
 - process data for analysis

april 20 2016
emily
'''

import json
import pandas as pd


f = '/Users/emilyhalket/Box Sync/GoT_data/data/twitter_stream_test_NYPrimary.txt'
tweets = []
tweets_file = open(f, "r")

for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets.append(tweet)
    except:
        pass


len(tweets) # 217,524 tweets? although it seems like each entry might have multiple tweets?
# or maybe just reactions associated