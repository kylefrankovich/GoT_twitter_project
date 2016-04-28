__author__ = 'kfranko'

# script to process tweets collected by winter_is_coming.py

import json
from pprint import pprint


import json
from datetime import datetime
import time
from pytz import timezone
import os

data_path = '/Users/kfranko/Box Sync/GoT_data/data'

fileName = 'name_counts_test2016_04_25-16_38_08.txt'

fName = os.path.join(data_path, fileName)

# try stream method on search tweets (it works)

tweets_search = []
tweets_file = open(fName, "r")

# remember to execute this as a whole block!

for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_search.append(tweet)
    except:
        pass
print 'tweets loaded, yo'

len(tweets_search)

tweets_search[999]['text']
tweets_search[999]['created_at']


# load stream data:

tweets = []
tweets_file = open(fName, "r")

# remember to execute this as a whole block!

for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets.append(tweet)
    except:
        pass
    print 'tweets loaded, yo'

len(data)

len(tweets) # 384,543 tweets from 4/24 premiere episode; streamed from just before 9PM eastern
# (~5:45 pacific/00:45 UTC) until 11PM eastern (~8:00 pacific/03:00 UTC); NB: tweet times are in UTC, which is 7
# hours ahead of pacific

tweets[384542]['text']

tweets[384542]['created_at']

# try to convert twitter date to a timestamp:

tweet = tweets[0]
# this works using 'import time' not 'from date time import time'
ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
# only hour/minute/second
ts = time.strftime('%H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))



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



customers = [{"uid":1,"name":"John"},
    {"uid":2,"name":"Smith"},
           {"uid":3,"name":"Andersson"},
            ]

print customers

for x in customers:
    print x["uid"], x["name"]


empty_list = []

for x in customers:
    empty_list.append({'test':x['name']})


# create a list of dictionaries; only include 'text' and 'created at' fields:

tweet_text_time = []

for x in tweets_search:
    tweet_text_time.append({'text':x['text'], 'timestamp':x['created_at']})



# start playing around with text processing:

# Import BeautifulSoup into your workspace
from bs4 import BeautifulSoup

# Initialize the BeautifulSoup object on a single movie review
example1 = BeautifulSoup(tweet_text_time[0]['text'])

# Print the raw review and then the output of get_text(), for
# comparison
print tweet_text_time[0]['text']
print example1.get_text()



# load name counts:

f = open(fName, 'r')
x = f.readlines()