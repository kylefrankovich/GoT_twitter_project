__author__ = 'kfranko'

# script to process tweets collected by winter_is_coming.py

import json
from pprint import pprint


import json
from datetime import datetime
from pytz import timezone

data_path = '/Users/kfranko/Box Sync/GoT_data/data'

fileName = 'twitter_stream_test_NYPrimary.txt'

fName = os.path.join(data_path, fileName)

# this method works; for explanation, see: http://stackoverflow.com/questions/12451431/loading-and-parsing-a-json-file-in-python
data = []
with open(fName) as f:
    for line in f:
        data.append(json.loads(line))

len(data)

data[0]['text']

data[0]['created_at'] # search api appears to start collecting from most recent (ex: data[0]) to earliest (ex: data[end]);
# other note: I'm pretty sure all times are given in GMT, don't think it's a big deal, but might have to account for this

# to convert from UTC/GMT: manually subtract 7 (for Pacific) or find automatic way?


data[0]['user']['name']
# print all keys in dict:

data[0].keys()

# for analysis, maybe we should use scikit learn's CountVectorizer?; can we have that search for a specific vocabulary
# (ex: only count the number of times a character name appears)?; although perhaps we want to manually do this to
# maintain the time information associated with the character name (ex: plotting the timeseries for the hour of the
# original broadcast; X person is killed, and we see an explosion of tweets regarding their death)


