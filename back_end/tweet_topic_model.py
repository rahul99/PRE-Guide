#!/usr/bin/python3

import sys, os
import numpy as np 
sys.path.append('./')
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle, json
import pandas as pd
import nltk, re
from nltk.corpus import stopwords
import subprocess
from models import book_topic_model


###################################################
# 			Pre-processing component 			  #
###################################################
def rm_html_tags(str):
    html_prog = re.compile(r'<[^>]+>',re.S)
    return html_prog.sub('', str)

def rm_html_escape_characters(str):
    pattern_str = r'&quot;|&amp;|&lt;|&gt;|&nbsp;|&#34;|&#38;|&#60;|&#62;|&#160;|&#20284;|&#30524;|&#26684|&#43;|&#20540|&#23612;'
    escape_characters_prog = re.compile(pattern_str, re.S)
    return escape_characters_prog.sub('', str)

def rm_at_user(str):
    return re.sub(r'@[a-zA-Z_0-9]*', '', str)

def rm_url(str):
    return re.sub(r'http[s]?:[/+]?[a-zA-Z0-9_\.\/]*', '', str)

def rm_repeat_chars(str):
    return re.sub(r'(.)(\1){2,}', r'\1\1', str)

def rm_hashtag_symbol(str):
    return re.sub(r'#', '', str)

def replace_emoticon(emoticon_dict, str):
    for k, v in emoticon_dict.items():
        str = str.replace(k, v)
    return str

def rm_time(str):
    return re.sub(r'[0-9][0-9]:[0-9][0-9]', '', str)

def rm_punctuation(current_tweet):
    return re.sub(r'[^\w\s]','',current_tweet)

def pre_process(str, porter):
    # do not change the preprocessing order only if you know what you're doing 
    str = str.lower()
    str = rm_url(str)
    str = rm_at_user(str)
    str = rm_repeat_chars(str) 
    str = rm_hashtag_symbol(str)       
    str = rm_time(str)
    str = rm_punctuation(str)
        
    try:
        str = nltk.tokenize.word_tokenize(str)
        try:
            str = [porter.stem(t) for t in str]
        except:
            #print(str)
            pass
    except:
        #print(str)
        pass
        
    return str

###################################################
# 		Tweet Classification Component			  #
###################################################
def get_topic_ids(tweets_list, tfidf_path, pca_path, mean_X_path, model_path, mode):
	model = joblib.load(model_path)
	pca = pickle.load(open(pca_path, 'rb'), encoding='latin1')
	tfidf_vocab = pickle.load(open(tfidf_path, 'rb'), encoding='latin1')
	MEAN_X = np.loadtxt(mean_X_path, dtype=float, delimiter=',')
	vectorizer = TfidfVectorizer(decode_error="replace", vocabulary=tfidf_vocab)

	porter = nltk.PorterStemmer()
	stops = set(stopwords.words('english'))
	stops.add('rt')

	if(mode == 'validate'):
		tweets_list = json.load(open(tweets_list))['tweets']

	X = []
	for tweet in tweets_list:
		tweet = pre_process(tweet.strip('\n'), porter)
		tweet = [word for word in tweet if word not in stops]
		X.append(' '.join(tweet))

	X = vectorizer.fit_transform(X)
	X = pca.transform(X.toarray())
	X = X - MEAN_X
	ids = model.predict(X)
	return(ids)


def main():

	mode = 'test' # one of "test" or "validate"

	if(mode == 'test'):
		json_string = sys.argv[1]
		json_string = json_string[1:-3]
		json_tweets = json.loads(json_sring)
		json_tweets = json_tweets['tweets']

	# directory setup
	proj_path = os.path.dirname(os.path.realpath(__file__))
	data_basepath = os.path.join(proj_path, 'data')
	model_basepath = os.path.join(proj_path, 'models')
	mean_X_feat = os.path.join(data_basepath, 'mean_X.txt')

	tfidf_feat = os.path.join(model_basepath, 'tfidf_features.pkl')
	pca_feat = os.path.join(model_basepath, 'pca_components.pkl')
	model_path = os.path.join(model_basepath, 'rf_model.pkl')

	goodbooks_path = os.path.join(proj_path, 'data/goodbooks')
	book2tag_path = os.path.join(goodbooks_path, 'book_tags.csv')
	book_data_path = os.path.join(goodbooks_path, 'books.csv')

	if(mode == 'validate'):
		json_tweets = os.path.join(data_basepath, 'test.json')

	ids = get_topic_ids(tweets_list=json_tweets,
						tfidf_path=tfidf_feat,
						pca_path=pca_feat,
						mean_X_path=mean_X_feat,
						model_path=model_path,
						mode=mode,
			  			)

	json_out = book_topic_model.top_recommended_books(tweet_labels=ids,
													  book2tag_path=book2tag_path,
													  book_data_path=book_data_path,
													 )

	print(json_out)

if __name__ == "__main__":
	main()