#!/usr/bin/python

import sys, os
import numpy as np 
sys.path.append('./')
from sklearn import metrics
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import sparse
import pickle
from time import time
from datetime import timedelta


def load(data_file, label_file):
	print("Loading data...")
	with open(data_file, 'r') as f:
		X = f.readlines()
	with open(label_file, 'r') as f:
		y = np.array(f.readlines())
	y = np.asarray(y, dtype=int)

	return(X, y)
	
def test(X_path, y_path, tfidf_path, pca_path, mean_X_path, model_path):
	model = joblib.load(model_path)
	pca = pickle.load(open(pca_path, 'rb'))
	tfidf_vocab = pickle.load(open(tfidf_path, 'rb'))
	MEAN_X = np.loadtxt(mean_X_path, dtype=float, delimiter=',')
	X, y = load(X_path, y_path)

	vectorizer = TfidfVectorizer(decode_error="replace", vocabulary=tfidf_vocab)
	X = vectorizer.fit_transform(X)

	# get principal components
	test_start = time()
	#X = sparse.csr_matrix.dot(X, np.transpose(pca))
	X = pca.transform(X.toarray())
	test_end = time()
	print("pca performance time: {}".format(timedelta(seconds=test_end-test_start)))

	X = X - MEAN_X

	test_start = time()
	pred = model.predict(X)
	test_end = time()
	f1 = metrics.f1_score(y, pred, average='macro')
	print("f1 using RF is: {} | test time: {}".format(f1, timedelta(seconds=test_end - test_start)))

if __name__ == "__main__":

	# directory setup
	proj_path = os.path.dirname(os.path.realpath(__file__))
	data_basepath = os.path.join(proj_path, 'data')
	model_basepath = os.path.join(proj_path, 'models')


	#################################################
	#				Test 20 newsgroup				#
	#################################################
	news_data = os.path.join(data_basepath, '20news_test_data.txt')
	news_labels = os.path.join(data_basepath, '20news_test_labels.txt')
	mean_X_feat = os.path.join(data_basepath, 'mean_X.txt')

	tfidf_feat = os.path.join(model_basepath, 'tfidf_features.pkl')
	pca_feat = os.path.join(model_basepath, 'pca_components.pkl')
	model_path = os.path.join(model_basepath, 'rf_model.pkl')

	test(X_path=news_data,
		 y_path=news_labels,
		 tfidf_path=tfidf_feat,
		 pca_path=pca_feat,
		 mean_X_path=mean_X_feat,
		 model_path=model_path,
		)
	print("Execution Complete")

