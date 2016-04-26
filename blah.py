__author__ = 'kfranko'



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
