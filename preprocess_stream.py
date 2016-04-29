'''

Developing a script to read in and preprocess streamed tweet info
April 29 2016

'''

import json
from nltk.tokenize import word_tokenize
import operator
from collections import Counter
from nltk.corpus import stopwords
import string
from nltk import bigrams
import datetime
import os
import re
import csv

'''
Set filename and path
'''
data_path = '/Users/emilyhalket/Box Sync/GoT_data/data'
fileName = 'GoT_tweet_stream_ep1_emily_04242016.txt'
fName = os.path.join(data_path, fileName)
save_path = '/Users/emilyhalket/Box Sync/GoT_data/data'
datestr = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
countFileOutName = 'GoT_name_counts_ep1_24_hrs_{}.txt'.format(datestr)
counter_output_file_fName = os.path.join(save_path, countFileOutName)


'''

 create functions to handle emoticons & punctuation

'''


emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']


'''

read in file of raw tweet data

'''


with open(f, 'r') as tweets_file:
    count_all_terms_stop = Counter()
    count_all_hash = Counter()
    count_all_terms_only = Counter()
    for line in tweets_file:
        try:
            tweet = json.loads(line)

            terms_stop = [term for term in preprocess(tweet['text'], lowercase=True) if term not in stop]

            # Count hash tags only
            terms_hash = [term for term in preprocess(tweet['text'], lowercase=True)
                          if term.startswith('#')]
            # Count terms only (no hash tags, no mentions)
            terms_only = [term for term in preprocess(tweet['text'], lowercase=True) if term not in stop and
                          not term.startswith(('#', '@'))]

            # Update the counter(s)
            count_all_terms_stop.update(terms_stop)
            count_all_hash.update(terms_hash)
            count_all_terms_only.update(terms_only)
        except:
            pass
    # Print the first 5 most frequent words
    print 'preprocessing/counting term frequency complete!'
    print 'most common w/ stops removed:', (count_all_terms_stop.most_common(5))
    print 'most hashtags:', (count_all_hash.most_common(5))
    print 'most terms_only:', (count_all_terms_only.most_common(5))


'''

 count character names

'''


character_names = ['tyrion', 'snow', 'arya', 'daenerys', 'sansa', 'cersei', 'joffrey',
                   'margaery', 'melisandre', 'bran', 'stannis', 'ramsay', 'theon', 'jaime',
                   'brienne', 'bronn', 'varys', 'davos', 'oberyn', 'daario', 'jorah', 'myrcella',
                   'tommen', 'tyene', 'tywin', 'roose', 'hodor', 'pod', 'podrick', 'mountain', 'gregor',
                   'hound', 'bran', 'khal', 'drogo', 'khaleesi']

name_dict = {}
for name in character_names:
    name_dict[name] = count_all_terms_stop[name]


names_csv = '/Users/emilyhalket/Box Sync/GoT_data/data/GoT_emily_stream_name_counts_ep1.csv'

with open(names_csv, 'wb') as f:  # Just use 'w' mode in 3.x
    w = csv.DictWriter(f, name_dict.keys())
    w.writeheader()
    w.writerow(name_dict)