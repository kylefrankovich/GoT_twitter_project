__author__ = 'kfranko'

import os

data_path = '/Users/kfranko/Box Sync/GoT_data/data/episode_10'

fileName = 'GoT_search_ep10_48_hrs_2016_06_29-12_16_25.txt'

fName = os.path.join(data_path, fileName)

from GoT_functions import tweet_loader, tweet_reducer

# reduce data for later processing:

tweet_reducer(fName, '10', 'search_48_hrs', 'kfranko', 'kyle')

# get character counts:

from GoT_functions import preprocess_character_counts

ep_num = '10'
user_name = 'kfranko'
search_type = 'search_48_hrs'
data_collector = 'kyle'

preprocess_character_counts(ep_num,user_name,search_type,data_collector)