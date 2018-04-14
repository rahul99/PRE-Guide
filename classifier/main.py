import sys
import json

# Get tweets as json string from command line argument
jsonString = sys.argv[1]    # jsonString = '{"tweets": ["This is tweet 1", "This is tweet 2"]}'
jsonString = jsonString[1:-3]
jsonTweets = json.loads(jsonString)

# Invoke your prediction algorithm here
# ...

# Return recommendations result as json object to node
jsonResults = {
	"newsgroup": "alt.atheism",
	"books": "11th-century",
	"recommendations": [
		"book title 1",
		"book title 2",
		"book title 3"
	]
}

# jsonTweetsDumps = json.dumps(jsonResults)
# jsonTweetsDumps = json.dumps(jsonTweets)
# print(jsonTweetsDumps)