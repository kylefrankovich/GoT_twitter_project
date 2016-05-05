"""

Functions for Processing GoT Tweet Data

Kyle Frankovich
Emily Halket

"""

import json
from collections import Counter
from nltk.corpus import stopwords
import string
import datetime
import os
import csv
import re
import pandas as pd


'''
tweet loader can read in raw or reduced twitter data
'''


def tweet_loader(input_file):
    # here we add our basic method for loading tweets from the list of json objects
    tweets = []  # create storage variable
    tweets_file = open(input_file, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets.append(tweet)
        except:
            pass
    print '{} tweets loaded, yo'.format(len(tweets))
    return tweets


'''
tweet_reducer is a function that loads in raw twitter data, which is a list of json objects that contain information
about each tweet (user profile, geo information, likes, RTs, etc...)

currently, outputs text and timestamp (variables of interest)

this allows us to archive raw data to free up shared storage space
'''


def tweet_reducer(input_file, episode_number, search_type, user_name, data_collector):
    output_file_name = '/Users/{}/Box Sync/GoT_data/data/episode_{}/ep_{}_{}_{}.txt'.format(user_name,episode_number,episode_number,data_collector,search_type)
    reduced_tweets = []  # create storage variable for reduced data
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


'''
    handle emoticons & punctuation for text pre processing
'''


def tokenize(tokens_re, s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):

    emoticons_str = r"""
        (?:
            [:=;] # Eyes
            [oO\-]? # Nose (optional)
            [D\)\]\(\]/\\OpP] # Mouth
        )"""
    regex_str = [
        emoticons_str,
        r'<[^>]+>',  # HTML tags
        r'(?:@[\w_]+)',  # @-mentions
        r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
        r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs

        r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
        r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
        r'(?:[\w_]+)',  # other words
        r'(?:\S)'  # anything else
    ]
    tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
    emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)
    tokens = tokenize(tokens_re, s)

    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


'''

Process text from 'reduced' file:
 - Writes csv with name counts - can add on this function to output other files/variables of interest
 - Name Library can be updated as characters are added
 - episode = episode number, points to folder where reduced data file lives
 - username = emilyhalket or kfranko
 - search_type = search or stream
 - data_collector = emily or kyle

'''


def preprocess_character_counts(episode, username, search_type, data_collector):

    """
    Set filename and path
    """

    data_path = '/Users/{}/Box Sync/GoT_data/data/'.format(username)
    file_name = 'episode_{}/ep_{}_{}_{}.txt'.format(episode, episode, data_collector, search_type)
    f = os.path.join(data_path, file_name)
    date_string = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    punctuation = list(string.punctuation)
    stop = stopwords.words('english') + punctuation + ['rt', 'via']
    char_file = 'character_names_library.csv'
    cf = os.path.join(data_path, char_file)

    '''
    read in file of raw tweet data
    '''

    tweets_file = open(f).read()
    tweet_list = json.loads(tweets_file)
    count_all_terms_stop = Counter()
    count_all_hash = Counter()
    count_all_terms_only = Counter()

    for tweet in tweet_list:

        terms_stop = [term for term in preprocess(tweet['text'],
                                                  lowercase=True) if term not in stop]
        # Count hash tags only
        terms_hash = [term for term in preprocess(tweet['text'],
                                                  lowercase=True)
                      if term.startswith('#')]
        # Count terms only (no hash tags, no mentions)
        terms_only = [term for term in preprocess(tweet['text'],
                                                  lowercase=True) if term not in stop and
                      not term.startswith(('#', '@'))]
        # Update the counter(s)
        count_all_terms_stop.update(terms_stop)
        count_all_hash.update(terms_hash)
        count_all_terms_only.update(terms_only)

    # Print the first 5 most frequent words
    print 'pre processing/counting term frequency complete!'
    print 'most common w/ stops removed:', (count_all_terms_stop.most_common(5))
    print 'most hash tags:', (count_all_hash.most_common(5))
    print 'most terms_only:', (count_all_terms_only.most_common(5))

    '''
    count character names
    '''

    char_names = pd.read_csv(cf)['name_to_match']

    name_dict = {}
    for name in char_names:
        name_dict[name] = count_all_terms_stop[name] + count_all_terms_stop['#' + name]
        # need to make it so that both 'arya' and '#arya' are counted as 'arya'

    names_csv = '/Users/{}/Box Sync/GoT_data/data/episode_{}/{}_GoT_ep{}_{}_name_counts{}.csv'.format(
        username, episode, data_collector, episode, search_type, date_string)

    with open(names_csv, 'wb') as f:
        w = csv.DictWriter(f, name_dict.keys())
        w.writeheader()
        w.writerow(name_dict)
