__author__ = 'kfranko'

import os

data_path = '/Users/kfranko/Box Sync/GoT_data/data/episode_1'

fileName = 'ep_1_kyle_search.txt'

fName = os.path.join(data_path, fileName)

from GoT_functions import tweet_loader, tweet_reducer


tweet_reducer(fName, '1', 'stream', 'kfranko', 'kyle')


episode_1_search_tweets = tweet_loader(fName)

len(episode_1_search_tweets[0])


# do character counts:

from GoT_functions import preprocess_character_counts

ep_num = '2'
user_name = 'kfranko'
search_type = 'stream'
data_collector = 'kyle'

preprocess_character_counts(ep_num,user_name,search_type,data_collector)