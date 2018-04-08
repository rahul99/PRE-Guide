import sys
import math
import json
from twitter_scraper import get_tweets

# Get username and number of tweets from command line arguments
username = str(sys.argv[1])
num_tweets = int(sys.argv[2])

# Compute number of pages to retrieve
# Each page has 20 tweets
num_pages = math.ceil(num_tweets / 20.0)

# Retrieve tweets by pages
json_tweet = {
    "tweets": []
}
for tweet in get_tweets(username, pages=num_pages):
    json_tweet['tweets'].append(tweet['text'])

# Remove unwanted tweets
json_tweet['tweets'] = json_tweet['tweets'][0:num_tweets]

# Dumps
json_tweet_dumps = json.dumps(json_tweet)

# Return tweets to Node server
print(json_tweet_dumps)