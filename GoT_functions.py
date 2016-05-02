__author__ = 'kfranko'


def tweet_loader(input_file):
    # here we add our basic method for loading tweets from the list of json objects
    for line in input_file:
        try:
            tweet = json.loads(line)
            tweets.append(tweet)
        except:
            pass

# x is a function that loads in raw twitter data, which is a list of json objects that contain information
# about each tweet (user profile, geo information, likes, RTs, etc... for now, we're only interested in
# the text of the tweet for natural language processing and the time at which the tweet was created for time
# series analysis)

def tweet_reducer(input_file, episode_number, search_type, user_name):
    data_path = '/Users/{}/Box Sync/GoT_data/data/episode_{}'.format(user_name,ep)
    output_file_name = '/Users/{}/Box Sync/GoT_data/data/episode_{}/{}_ep_{}_{}.txt'.format(user_name,ep,user_name,episode_number,search_type)
    load_tweet_data(input_file) # something like this... still need to write the function (based on emily's file)
    empty_list = []
    # create a dictionary of two items that we'll want (ex: tweet text and tweet time)
    for tweet in input_file:
        empty_list.append({'name':x['name'], 'UID':x['uid']})