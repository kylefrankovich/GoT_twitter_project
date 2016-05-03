'''

Developing a script to read in and preprocess streamed tweet info
April 29 2016

'''

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
    handle emoticons & punctuation
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


def preprocess_character_counts(episode, username, search_type, data_collector):

    # episode = episode number, points to folder where reduced data file lives
    # username = emilyhalket or kfranko
    # search_type = search or stream
    # data_collector = emily or kyle

    """
    Set filename and path
    """

    data_path = '/Users/{}/Box Sync/GoT_data/data/'.format(username)
    file_name = 'episode_{}/ep_{}_{}_{}.txt'.format(episode, episode, data_collector, search_type)
    f = os.path.join(data_path, file_name)
    date_string = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    punctuation = list(string.punctuation)
    stop = stopwords.words('english') + punctuation + ['rt', 'via']

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

    char_file = 'character_names_library.csv'
    cf = os.path.join(data_path, char_file)

    char_names = pd.read_csv(cf)['name_to_match']

    name_dict = {}
    for name in char_names:
        name_dict[name] = count_all_terms_stop[name]

    names_csv = '/Users/{}/Box Sync/GoT_data/data/episode_{}/{}_GoT_ep{}_{}_name_counts{}.csv'.format(
        username, episode, data_collector, episode, search_type, date_string
    )

    with open(names_csv, 'wb') as f:  # Just use 'w' mode in 3.x
        w = csv.DictWriter(f, name_dict.keys())
        w.writeheader()
        w.writerow(name_dict)