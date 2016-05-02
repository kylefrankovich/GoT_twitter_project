__author__ = 'kfranko'


file_to_load = '/Users/kfranko/Box Sync/GoT_data/data/test_files/earthday_2016_04_23-17_36_00.txt'

from GoT_functions import tweet_loader

test_load_data = tweet_loader(file_to_load)

test_load_data[0]['text'] # it works!

len(test_load_data)

# now let's test the tweet reducer:

from GoT_functions import tweet_reducer

tweet_reducer(file_to_load, '1', 'search', 'kfranko')

# now try reading in the reduced file using tweet_loader:

reduced_file_to_load = '/Users/kfranko/Box Sync/GoT_data/data/episode_1/kfranko_ep_1_search.txt'

test_load_data_reduced = tweet_loader(reduced_file_to_load)

len(test_load_data_reduced)

test_load_data_reduced[0][0]
test_load_data_reduced[0][0]['text']



