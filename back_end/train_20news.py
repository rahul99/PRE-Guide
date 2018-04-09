#!/usr/bin/python

import sys, os
import numpy as np 
sys.path.append('./')
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib
import numpy as np
import re
import argparse
from scipy import sparse
import pickle
from time import time
from datetime import timedelta

###################################################
# 					static files 				  #
###################################################
news_cat_ids = np.arange(20)
news_cat_name = ['alt.atheism',
 'comp.graphics',
 'comp.os.ms-windows.misc',
 'comp.sys.ibm.pc.hardware',
 'comp.sys.mac.hardware',
 'comp.windows.x',
 'misc.forsale',
 'rec.autos',
 'rec.motorcycles',
 'rec.sport.baseball',
 'rec.sport.hockey',
 'sci.crypt',
 'sci.electronics',
 'sci.med',
 'sci.space',
 'soc.religion.christian',
 'talk.politics.guns',
 'talk.politics.mideast',
 'talk.politics.misc',
 'talk.religion.misc']
tweet_id2cat = dict(zip(news_cat_ids, news_cat_name)) 


def train(X, y, model_path):

	# SVM
	model = SVC(C=1, kernel='linear', degree=4, gamma='auto', coef0=0.0, shrinking=True,
	probability=False, tol=0.001, cache_size=200, class_weight='balanced', verbose=False,
	max_iter=-1, decision_function_shape='ovr', random_state=None)
	train_start = time()
	model.fit(X, y)
	train_end = time()
	test_start = time()
	pred = model.predict(X)
	test_end = time()
	f1 = metrics.f1_score(y, pred, average='macro')
	print("f1 using SVM is: {} | train time: {} | test time: {}".format(f1, timedelta(seconds=train_end-train_start), timedelta(seconds=test_end - test_start)))

	# Passive Aggressive
	model = PassiveAggressiveClassifier(C=1.0, fit_intercept=True, max_iter=None, tol=0.001,
	shuffle=True, verbose=0, loss='hinge', n_jobs=1, random_state=None, warm_start=False,
	class_weight='balanced', average=True, n_iter=None)	
	train_start = time()
	model.fit(X, y)
	train_end = time()
	test_start = time()
	pred = model.predict(X)
	test_end = time()
	f1 = metrics.f1_score(y, pred, average='macro')
	print("f1 using PA is: {} | train time: {} | test time: {}".format(f1, timedelta(seconds=train_end-train_start), timedelta(seconds=test_end - test_start)))

	# SGD Classifier
	model = SGDClassifier(loss='hinge', penalty='l2', alpha=0.0001, l1_ratio=0.15, fit_intercept=True,
	max_iter=None, tol=0.001, shuffle=True, verbose=0, epsilon=0.1, n_jobs=1, random_state=None,
	learning_rate='optimal', eta0=0.0, power_t=0.5, class_weight=None, warm_start=False, average=False, n_iter=None)
	train_start = time()
	model.fit(X, y)
	train_end = time()
	test_start = time()
	pred = model.predict(X)
	test_end = time()
	f1 = metrics.f1_score(y, pred, average='macro')
	print("f1 using SGD is: {} | train time: {} | test time: {}".format(f1, timedelta(seconds=train_end-train_start), timedelta(seconds=test_end - test_start)))

	# RF Classifier
	model = RandomForestClassifier(n_estimators=100)
	train_start = time()
	model.fit(X, y)
	train_end = time()
	test_start = time()
	pred = model.predict(X)
	test_end = time()
	f1 = metrics.f1_score(y, pred, average='macro')
	print("f1 using RF is: {} | train time: {} | test time: {}".format(f1, timedelta(seconds=train_end-train_start), timedelta(seconds=test_end - test_start)))
	joblib.dump(model, model_path) 
	return(model)

def load(data_file, label_file, mean_X_file=None):
	print("Loading data...")
	X = np.loadtxt(data_file, dtype=float, delimiter=',')

	if(mean_X_file):
		MEAN_X = np.mean(X, axis=0)
		np.savetxt(mean_X_file, MEAN_X, delimiter=',')
		X = X - MEAN_X

	with open(label_file, 'r') as f:
		y = np.array(f.readlines())
	y = np.asarray(y, dtype=int)
	print("Data: {} | Lables: {}".format(X.shape, y.shape))
	return(X, y)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-m', '--mode', default='all', type=str,
	                    metavar='MODE', help='mode | train or test')

	global args
	args = parser.parse_args()

	# directory setup
	proj_path = os.path.dirname(os.path.realpath(__file__))
	data_basepath = os.path.join(proj_path, 'data')
	model_basepath = os.path.join(proj_path, 'models')


	#################################################
	# 			  Train 20 newsgroup				#
	#################################################
	if(args.mode == 'train'):
		print("training model on 20news train data...")
		news_data_processed = os.path.join(data_basepath, '20news_traindata_processed.txt')
		news_labels = os.path.join(data_basepath, '20news_train_labels.txt')
	else:
		print("training model on 20news all data...")		
		news_data_processed = os.path.join(data_basepath, '20news_alldata_processed.txt')
		news_labels = os.path.join(data_basepath, '20news_all_labels.txt')

	mean_X_path = os.path.join(data_basepath, 'mean_X.txt')
	model_path = os.path.join(model_basepath, 'rf_model.pkl')
	X, y = load(news_data_processed, news_labels, mean_X_path)
	print("training models...")
	model = train(X,y, model_path)
	print("Execution Complete")