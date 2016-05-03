__author__ = 'kfranko'

import json


def tweet_loader(input_file):
    # here we add our basic method for loading tweets from the list of json objects
    tweets = [] # create storage variable
    tweets_file = open(input_file, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets.append(tweet)
        except:
            pass
    print '{} tweets loaded, yo'.format(len(tweets))
    return tweets


# tweet_reducer is a function that loads in raw twitter data, which is a list of json objects that contain information
# about each tweet (user profile, geo information, likes, RTs, etc... for now, we're only interested in
# the text of the tweet for natural language processing and the time at which the tweet was created for time
# series analysis)

def tweet_reducer(input_file, episode_number, search_type, user_name, data_collector):
    output_file_name = '/Users/{}/Box Sync/GoT_data/data/episode_{}/ep_{}_{}_{}.txt'.format(user_name,episode_number,episode_number,data_collector,search_type)
    reduced_tweets = [] # create storage variable for reduced data
    # here we add our basic method for loading tweets from the list of json objects
    tweets_file = open(input_file, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            reduced_tweets.append({'text':tweet['text'], 'created_at':tweet['created_at']})
        except:
            pass
    # export reduced data to a text file:
    json.dump(reduced_tweets, open(output_file_name,'w'))
    print '{} tweets reduced, yo'.format(len(reduced_tweets))