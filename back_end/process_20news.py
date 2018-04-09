#!/usr/bin/python

import sys, os
import numpy as np 
sys.path.append('./')
from sklearn.datasets import fetch_20newsgroups
import nltk
#nltk.download()
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from nltk.corpus import stopwords
from sklearn import metrics
import numpy as np
import re, pickle, argparse
from tqdm import tqdm

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

def vectorize_and_transform(in_data_file, in_label_file, out_data_file, out_tfidf_file, out_pca_file):
	print("Loading data...")
	with open(in_data_file, 'r') as f:
		X = f.readlines()
	with open(in_label_file, 'r') as f:
		y = np.array(f.readlines())

	X = np.asarray(X)
	y = np.asarray(y, dtype=int)

	vectorizer = TfidfVectorizer()
	X = vectorizer.fit_transform(X)

	with open(out_tfidf_file, 'wb') as f:
		pickle.dump(vectorizer.vocabulary_, f)

	# PCA on train. Transform and save principal components for inference
	print("Performing PCA...")
	pca = PCA(n_components=args.pca_components, whiten=True)
	X = pca.fit_transform(X.toarray())
	np.savetxt(out_data_file, X, delimiter=',')

	with open(out_pca_file, 'wb') as f:
		pickle.dump(pca, f)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-m', '--mode', default='all', type=str,
	                    metavar='MODE', help='mode | train or test')

	parser.add_argument('-u', '--use_filter', default=True, type=bool, metavar='Type',
	                    help='if True (default) remove header, footer and quotes from the data')

	parser.add_argument('-pc', '--pca_components', default=500, type=float,
	                    metavar='PCA', help='number of principal components')
	global args
	args = parser.parse_args()

	# directory setup
	proj_path = os.path.dirname(os.path.realpath(__file__))
	data_basepath = os.path.join(proj_path, 'data')
	model_path = os.path.join(proj_path, 'models')

	#########################################################
	#		Get list of unique words from the dataset		#
	#########################################################
	vocab_path = os.path.join(data_basepath, '20news_vocab.pkl')
	if(args.mode == 'train'):
		print("processing 20 newsgroup train data...")
		news_datapath = os.path.join(data_basepath, '20news_train_data.txt')
		news_datalabels = os.path.join(data_basepath, '20news_train_labels.txt')
	elif(args.mode == 'test'):
		print("processing 20 newsgroup test data...")
		news_datapath = os.path.join(data_basepath, '20news_test_data.txt')
		news_datalabels = os.path.join(data_basepath, '20news_test_labels.txt')
	else:
		print("processing 20 newsgroup all data...")
		news_datapath = os.path.join(data_basepath, '20news_all_data.txt')
		news_datalabels = os.path.join(data_basepath, '20news_all_labels.txt')

	porter = nltk.PorterStemmer()
	stops = set(stopwords.words('english'))
	stops.add('rt')

	get_20news_vocab_and_data(porter=porter,
							  stops=stops,
							  vocab_path=vocab_path,
							  data_path=news_datapath,
							  data_labels=news_datalabels,
							  )

	#########################################################
	# 	TF-IDF vectorize and transform data 				#
	# 	Save TF-IDF and pca features for use in inference	#
	#########################################################
	if(args.mode == 'train'):
		news_data = os.path.join(data_basepath, '20news_train_data.txt')
		news_data_processed = os.path.join(data_basepath, '20news_traindata_processed.txt')
		news_labels = os.path.join(data_basepath, '20news_train_labels.txt')
		tfidf_feat = os.path.join(model_path, 'tfidf_features.pkl')
		pca_feat = os.path.join(model_path, 'pca_components.pkl')

		vectorize_and_transform(in_data_file=news_data,
								in_label_file=news_labels,
								out_data_file=news_data_processed,
								out_tfidf_file=tfidf_feat,
								out_pca_file=pca_feat,
								)

	if(args.mode == 'all'):
		news_data = os.path.join(data_basepath, '20news_all_data.txt')
		news_data_processed = os.path.join(data_basepath, '20news_alldata_processed.txt')
		news_labels = os.path.join(data_basepath, '20news_all_labels.txt')
		tfidf_feat = os.path.join(model_path, 'tfidf_features.pkl')
		pca_feat = os.path.join(model_path, 'pca_components.pkl')

		vectorize_and_transform(in_data_file=news_data,
								in_label_file=news_labels,
								out_data_file=news_data_processed,
								out_tfidf_file=tfidf_feat,
								out_pca_file=pca_feat,
								)

	print("execution complete")


