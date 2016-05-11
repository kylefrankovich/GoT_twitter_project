__author__ = 'kfranko'

import os

data_path = '/Users/kfranko/Box Sync/GoT_data/data/episode_3'

fileName = 'GoT_search_ep3_48_hrs_2016_05_10-18_00_05.txt'

fName = os.path.join(data_path, fileName)

from GoT_functions import tweet_loader, tweet_reducer


tweet_reducer(fName, '3', 'search_48_hrs', 'kfranko', 'kyle')


episode_1_search_tweets = tweet_loader(fName)

len(episode_1_search_tweets[0])


# do character counts:

from GoT_functions import preprocess_character_counts

ep_num = '2'
user_name = 'kfranko'
search_type = 'search_48_hrs'
data_collector = 'kyle'

preprocess_character_counts(ep_num,user_name,search_type,data_collector)
