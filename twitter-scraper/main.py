import sys
import math
import unidecode
from twitter_scraper import get_tweets

# Get username and number of tweets from command line arguments
username = str(sys.argv[1])
num_tweets = int(sys.argv[2])

# Compute number of pages to retrieve
# Each page has 20 tweets
num_pages = math.ceil(num_tweets / 20.0)

# Retrieve tweets by pages
tweets = []
for tweet in get_tweets(username, pages=num_pages):
    tweets.append(tweet['text'])

# Remove unwanted tweets
tweets = tweets[0:num_tweets]

# Return tweets to Node server
# print(str(tweets))
print(unidecode.unidecode_expect_nonascii(str(tweets)))
# sys.stdout.flush()