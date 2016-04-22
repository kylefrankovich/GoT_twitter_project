__author__ = 'kfranko'

''' twitter webscraping project to analyze tweets timelocked to episodes in the new season of Game of Thrones;
idea is to collect all tweets using the GoT hashtag, and then process the text w/in each tweet to get a count
of  character mentions, and to plot these numbers in reference to episode events '''

# this method uses Application only Auth, as opposed to user auth, which has a greater
# rate limit; so here we can do 450 requests per second, with 100 tweets returned per request
# giving us a rate of 45,000 tweets every 15 minutes; if we want to get up to a million tweets per
# episode: we get 45,000 * 4 = 180000 tweets per hour; 1000000/180000 = 5.5 hours run time; do we
# expect more than a million in, let's say, 24 hours? seems likely, might need to break up scraping
# into multiple searches (i.e. one for day before, one for 24 hours following, one for immediately following airing
# (to guarantee that we can do a "live" analysis); of course, after the premiere we should have a better idea of
# twitter volume)

# http://www.karambelkar.info/2015/01/how-to-use-twitters-search-rest-api-most-effectively./

import tweepy
import datetime
import yaml
f = open('secrets.yaml')
# use safe_load instead load
API_info = yaml.safe_load(f)


API_KEY = API_info['key']
API_SECRET = API_info['secret']

# Replace the API_KEY and API_SECRET with your application's key and secret.
auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True,
				   wait_on_rate_limit_notify=True)

if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)

# Continue with rest of code

import sys
import jsonpickle
import os

# searchQuery = '#someHashtag'  # this is what we're searching for
searchQuery = '#UnbreakableKimmySchmidt'  # this is what we're searching for
# maxTweets = 10000000 # Some arbitrary large number
maxTweets = 1000 # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits
save_path = '/Users/kfranko/Box Sync/GoT_data/data'
datestr = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
fileName = 'unbreakable_{}.txt'.format(datestr) # We'll store the tweets in a text file.
paramFileName = 'script_parameters_{}.txt'.format(datestr) # let's output the parameters used for each search in small text file
fName = os.path.join(save_path, fileName)
script_parameters_fName =os.path.join(save_path, paramFileName)

# 'since' and 'until' parameters can be used to restrict the timeframe of the search
# Until - Returns tweets created before the given date. Date should be formatted as YYYY-MM-DD.
# Keep in mind that the search index has a 7-day limit. In other words, no tweets will
# be found for a date older than one week.
# Example Values: 2015-07-19

# last democratic debate was held on Thursday, April 14

search_from_date = None

search_to_date = None

# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
sinceId = None

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1L

tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))
print '\rscript start time is:', datetime.datetime.now()
time_start = datetime.datetime.now()
with open(fName, 'w') as f:
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry, since = search_from_date, until = search_to_date)
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            since_id=sinceId, since = search_from_date, until = search_to_date)
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1), since = search_from_date, until = search_to_date)
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId, since = search_from_date, until = search_to_date)
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                f.write(jsonpickle.encode(tweet._json, unpicklable=False) +
                        '\n')
            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))
print '\rscript end time is:', datetime.datetime.now()
time_stop = datetime.datetime.now()
total_runtime = time_stop - time_start
print '\rtotal script runtime is:', total_runtime

# output parameters of the search that was just completed:

script_parameters_file = open(script_parameters_fName, "w")
script_parameters_file.writelines(["search query: {0}\n".format(searchQuery),
                "time start: {0}\n".format(time_start),
                "time stop: {0}\n".format(time_stop),
                "total run time: {0}\n".format(total_runtime),
                "max tweets: {0}\n".format(maxTweets),
                "output file name: {0}\n".format(fileName),
                "search from date: {0}\n".format(search_from_date),
                "search to date: {0}\n".format(search_to_date),
                "number of tweets: {0}\n".format(tweetCount)]
)
script_parameters_file.close()

# remaining issues: we need to set a time limit (i.e. search from time episode begins (or before it starts?) to 24 hours after);
# also, can we automate the script to run on it's own?; ask Nick, perhaps we need to have the script running on a server...