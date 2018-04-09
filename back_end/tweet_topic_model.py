#!/usr/bin/python

import sys, os
import numpy as np 
sys.path.append('./')
from sklearn import metrics
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import sparse
import pickle, json
from time import time
import nltk, re
from nltk.corpus import stopwords
from datetime import timedelta


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
            print(str)
            pass
    except:
        print(str)
        pass
        
    return str

def get_20news_vocab_and_data(porter, stops, vocab_path, data_path, data_labels):
	if(args.use_filter):
		remove = ('headers', 'footers', 'quotes')
	else:
		remove = ()

	newsgroups = fetch_20newsgroups(subset=args.mode, remove=remove)

	vocab = []; data = []
	with open(data_path, 'w') as f:
		for i in tqdm(range(len(newsgroups.data))):
			news_i = newsgroups.data[i]
			news_i = pre_process(news_i, porter)
			news_i = [word for word in news_i if word not in stops]
			f.write('%s\n' %news_i) # write new data to file
			vocab.append(list(set(news_i))) # maintain unique words in a vocab

	# write labels into file
	np.savetxt(data_labels, newsgroups.target, delimiter=',', fmt='%i')

	# write vocabulary into file
	if(args.mode == 'train'):
		flatten = lambda l: [item for sublist in l for item in sublist]
		vocab = flatten(vocab)
		vocab = list(set(vocab))
		with open(vocab_path, 'w') as f:
			pickle.dump(vocab, f)


def get_topic_ids(tweets, tfidf_path, pca_path, mean_X_path, model_path):
	model = joblib.load(model_path)
	pca = pickle.load(open(pca_path, 'rb'))
	tfidf_vocab = pickle.load(open(tfidf_path, 'rb'))
	MEAN_X = np.loadtxt(mean_X_path, dtype=float, delimiter=',')
	vectorizer = TfidfVectorizer(decode_error="replace", vocabulary=tfidf_vocab)

	porter = nltk.PorterStemmer()
	stops = set(stopwords.words('english'))
	stops.add('rt')

	tweets_list = json.load(open(tweets))['tweets']
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

if __name__ == "__main__":

	#json_tweets = sys.argv[1]

	# directory setup
	proj_path = os.path.dirname(os.path.realpath(__file__))
	data_basepath = os.path.join(proj_path, 'data')
	model_basepath = os.path.join(proj_path, 'models')
	mean_X_feat = os.path.join(data_basepath, 'mean_X.txt')

	tfidf_feat = os.path.join(model_basepath, 'tfidf_features.pkl')
	pca_feat = os.path.join(model_basepath, 'pca_components.pkl')
	model_path = os.path.join(model_basepath, 'rf_model.pkl')

	json_tweets = os.path.join(data_basepath, 'test.json')

	ids = get_topic_ids(tweets=json_tweets,
				 tfidf_path=tfidf_feat,
				 pca_path=pca_feat,
				 mean_X_path=mean_X_feat,
				 model_path=model_path,
			  		 )

	print ids
	