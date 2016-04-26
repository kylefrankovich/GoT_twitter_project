__author__ = 'kfranko'

# much thanks to Marco Bonzanini, data scientist from the UK, who helped me out
# with some information about collecting twitter data and for his example scripts
# for preprocessing, on which some of this work is based:

from nltk.tokenize import word_tokenize
import json
import operator
from collections import Counter
from nltk.corpus import stopwords
import string
from nltk import bigrams
import datetime
import os

data_path = '/Users/kfranko/Box Sync/GoT_data/data'
fileName = 'kf_GoT_stream_04_24_16.txt'
fName = os.path.join(data_path, fileName)
save_path = '/Users/kfranko/Box Sync/GoT_data/data'
datestr = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
countFileOutName = 'name_counts_ep1{}.txt'.format(datestr)
counter_output_file_fName = os.path.join(save_path, countFileOutName)


# import the streamed/searched data:

tweets_search = []
tweets_file = open(fName, "r")

f = open(fName, "r")

# remember to execute this as a whole block!

for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_search.append(tweet)
    except:
        pass
print 'tweets loaded, yo'

tweet = tweets[6355]['text']
print(word_tokenize(tweet))
# ['RT', '@', 'marcobonzanini', ':', 'just', 'an', 'example', '!', ':', 'D', 'http', ':', '//example.com', '#', 'NLP']


# need to deal with particularities of tweets (@s, hashtags, emoticons, etc...); we'll use regular expressions:

import re

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

tweet = "RT @marcobonzanini: just an example! :D http://example.com #NLP"
print(preprocess(tweet))
# ['RT', '@marcobonzanini', ':', 'just', 'an', 'example', '!', ':D', 'http://example.com', '#NLP']


# process all tweets from the stream or search list:

with open(fName) as f:
    for line in f:
        tweet = json.loads(line)
        tokens = preprocess(tweet['text'])
        #do_something_else(tokens)


# probably a good idea to remove stop words since we don't care about their count;
# also remove 'rt' and 'via', two words common to twitter (maybe add more later
# once we get a look at our data?):

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']


# load data and perform preprocessing/counting:


with open(fName, 'r') as f:
    count_all_terms_stop = Counter()
    count_all_hash = Counter()
    count_all_terms_only = Counter()
    for line in f:
        tweet = json.loads(line)
        # Create a list with all the terms
        # terms_all = [term for term in preprocess(tweet['text'])]
        terms_stop = [term for term in preprocess(tweet['text'], lowercase=True) if term not in stop]
        # terms_bigram = bigrams(terms_stop) # bigrams: sequences of two terms
        # Count terms only once, equivalent to Document Frequency
        # terms_single = set(terms_all)
        # Count hashtags only
        terms_hash = [term for term in preprocess(tweet['text'], lowercase=True)
                      if term.startswith('#')]
        # Count terms only (no hashtags, no mentions)
        terms_only = [term for term in preprocess(tweet['text'], lowercase=True)
              if term not in stop and
              not term.startswith(('#', '@'))]
              # mind the ((double brackets))
              # startswith() takes a tuple (not a list) if
              # we pass a list of inputs
        # Update the counter(s)
        count_all_terms_stop.update(terms_stop)
        count_all_hash.update(terms_hash)
        count_all_terms_only.update(terms_only)
    # Print the first 5 most frequent words
    print 'preprocessing/counting term frequency complete!'
    print 'most common w/ stops removed:', (count_all_terms_stop.most_common(5))
    print 'most hashtags:', (count_all_hash.most_common(5))
    print 'most terms_only:', (count_all_terms_only.most_common(5))

# save the counter data for later use:

character_names = ['kimmy', 'titus', 'jacqueline', 'lillian', 'xan', 'xanthippe', 'gretchen', 'reverend']

character_names = ['tyrion', 'snow', 'arya', 'daenerys', 'sansa', 'cersei', 'joffrey',
                   'margaery', 'melisandre', 'bran', 'stannis', 'ramsay', 'theon', 'jaime',
                   'brienne', 'bronn', 'varys', 'davos', 'oberyn', 'daario', 'jorah', 'myrcella',
                   'tommen', 'tyene', 'tywin', 'roose', 'hodor', 'pod', 'podrick', 'mountain', 'gregor',
                   'hound', 'bran', 'khal', 'drogo', 'khaleesi']


for name in character_names:
    print name, count_all_terms_stop[name]



# this works, will only print out "name value":
with open(counter_output_file_fName, 'w') as f:
    for name in character_names:
        f.write( "{} {}\n".format(name,count_all_terms_stop[name]) )




# test print out results of counter:
# also works, but need to make sure it's working properly
import pickle
with open(counter_output_file_fName, 'wb') as outputfile:
    pickle.dump(count_all_terms_stop, outputfile)


script_parameters_file = open(script_parameters_fName, "w")

with open(counter_output_file_fName, 'w') as f:
    for k,v in count_all_terms_stop():
        f.write( "{} {}\n".format(k,v) )




# when a counter object is populated, values are retrieved using dictionary API
# (ex: count_all_terms_stop['#unbreakablekimmyschmidt'])


