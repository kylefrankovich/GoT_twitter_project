__author__ = 'kfranko'

import os

data_path = '/Users/kfranko/Box Sync/GoT_data/data/episode_2'

fileName = 'kfranko_episode_2_stream.txt'

fName = os.path.join(data_path, fileName)

from GoT_functions import tweet_loader, tweet_reducer


tweet_reducer(fName, '2', 'stream', 'kfranko', 'kyle')


reduced_ep_1_search_tweets = tweet_loader(fName)

reduced_ep_1_search_tweets = reduced_ep_1_search_tweets[0]

len(reduced_ep_1_search_tweets)

# having issue with reducing streamed tweets. let's troubleshoot:

tweets_ep2 = tweet_loader(fName)
​
reduced_tweets2 = []
​
for tweet in tweets_ep1:
    reduced_tweets1.append({'text': tweet['text'], 'created_at': tweet['created_at']})
​
for tweet in tweets_ep2:
    reduced_tweets2.append({'text': tweet['text'], 'created_at': tweet['created_at']})

len(reduced_tweets2)

tweets_ep2[4415]

some_number = 666
print '{} tweets reduced, yo'.format(some_number)