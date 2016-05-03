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



# try making a small list of twitter data to figure out the indexing issue:

test_load_data[0]['text'] # it works!

range(2)

empty_list = []
# create a dictionary of two items that we'll want (ex: tweet text and tweet time)
for x in range(2):
    empty_list.append({'text':test_load_data[x]['text'], 'created_at':test_load_data[x]['created_at']})


test_output_fname = '/Users/kfranko/Desktop/empty_list_test_output.txt'
json.dump(empty_list, open(test_output_fname,'w'))

test_load_empty_list = tweet_loader(test_output_fname) # this causes the same weird indexing issue with the output of reducer

# weird indexing due to tweet_loader reading in a list [{},{},{}] into another empty list

#### indexing issue solved ####

data_test = test_load_empty_list[0] # do this when loading in reduced data in order to index normally:

data_test[0]

for tweet in data_test:
    print tweet['created_at']
