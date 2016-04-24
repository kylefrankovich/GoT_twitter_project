__author__ = 'kfranko'

# script to process tweets collected by winter_is_coming.py

import json
from pprint import pprint


import json
from datetime import datetime
from pytz import timezone
import os

data_path = '/Users/kfranko/Box Sync/GoT_data/data'

fileName = 'earthday_2016_04_23-17_36_00.txt'

fName = os.path.join(data_path, fileName)

# this method works; for explanation, see: http://stackoverflow.com/questions/12451431/loading-and-parsing-a-json-file-in-python
data = []
with open(fName) as f:
    for line in f:
        data.append(json.loads(line)) # makes a list of dictionaries

len(data)

data[0]['text']

data[0]['created_at'] # search api appears to start collecting from most recent (ex: data[0]) to earliest (ex: data[end]);
# other note: I'm pretty sure all times are given in GMT, don't think it's a big deal, but might have to account for this

# to convert from UTC/GMT: manually subtract 7 (for Pacific) or find automatic way?


data[0]['user']['name']
# print all keys in dict:

data[0].keys()

tweet_text = data[0:5]['text']

# for analysis, maybe we should use scikit learn's CountVectorizer?; can we have that search for a specific vocabulary
# (ex: only count the number of times a character name appears)?; although perhaps we want to manually do this to
# maintain the time information associated with the character name (ex: plotting the timeseries for the hour of the
# original broadcast; X person is killed, and we see an explosion of tweets regarding their death)


for tweet in data:
    # now tweet is a dictionary
    for attribute, value in tweet.iteritems():
        print attribute, value # example usage


# let's start working on a function to read in the tweet data and extract the useful
# information: namely, the tweet text (data[X]['text']) and the tweet time (data[X]['created_at']):

tweet_text = []
def extract_text(input_data):
    print len(input_data)-1
    for e in range(0,(len(input_data)-1)):
        tweet_text[e] = input_data[e]['text']
    return tweet_text


extract_text(data)