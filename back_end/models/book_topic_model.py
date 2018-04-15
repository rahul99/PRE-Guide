#!/usr/bin/python3

import sys, os
import numpy as np 
sys.path.append('./')
import pickle, json
import pandas as pd

###################################################
# 					static files 				  #
###################################################
news_ids = np.arange(20)
news_name = ['alt.atheism',
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
tweet_id2cat = dict(zip(news_ids, news_name))

tag_ids = [3308, 11284, 7939, 7939, 7939, 7939, 26497, 3624, 20527, 3956, 14681, 10583, 10385, 19634, 28247, 7116, 13801, 19991, 23931, 25647]
tag_names = ['Athesim',
'Cryptography',
'Computers',
'Computers',
'Computers',
'Computers',
'salem-witch-trials',
'Automobiles',
'Motorcycle-Club',
'Baseball',
'Hockey',
'Cryptography',
'Electronics',
'Medical Science',
'Science Fiction',
'Christanity',
'Weapons',
'Middle East',
'Politics',
'Religion']

#Space Opera -> clubbed to Science Fiction

tweet2tag_map = dict(zip(news_ids, tag_ids))

tag_id2name = dict(zip(tag_ids, tag_names))


def top_recommended_books(tweet_labels, book2tag_path, book_data_path, books_per_tag = 1):
	book_data = pd.read_csv(book_data_path, header='infer', sep=',')
	book_tag_count = pd.read_csv(book2tag_path, header='infer', sep=',')

	book_meta_list = []
	uniq_book_ids = []
	relevant_tag_list = []

	'''
	for id in tweet_labels:
		print("news: ({}){} | book: ({}){}".format(id, tweet_id2cat[id], tweet2tag_map[id], tag_id2name[tweet2tag_map[id]]))
	exit(0)
	'''

	for tweet_label in set(tweet_labels):
		tag_id = tweet2tag_map[tweet_label]
		subset = book_tag_count.loc[(book_tag_count['tag_id'] == tag_id)].sort_values(by='count', ascending=False)
		#subset.head()
		top_book_ids = subset['goodreads_book_id'][:books_per_tag].values.tolist() # pick the top book for a particular category
		for input_id in top_book_ids:
			book_dict = book_data.loc[book_data['goodreads_book_id'] == input_id].to_dict()
			book_id_dict = book_dict['book_id']
			book_id = list(book_id_dict.values())[0]
			if(book_id not in uniq_book_ids): # Store only the unique books
				uniq_book_ids.append(book_id)
				book_meta_list.append(book_dict)
				if(tag_id2name[tag_id] not in relevant_tag_list): # store unique tags for display
					relevant_tag_list.append(tag_id2name[tag_id])


	if(len(book_meta_list) > 4):
		if(len(relevant_tag_list) > 4):
			output_json = json.dumps({'books':book_meta_list[:4], 'tags':relevant_tag_list[:4]})
		else:
			output_json = json.dumps({'books':book_meta_list[:4], 'tags':relevant_tag_list})
	else:
		output_json = json.dumps({'books':book_meta_list, 'tags':relevant_tag_list})
	return(output_json)

if __name__ == "__main__":

	tweet_labels = sys.argv[1:]
	if(type(tweet_labels[0]) == str):
		tweet_labels = [int(item) for item in tweet_labels]

	# directory setup
	model_path = os.path.dirname(os.path.realpath(__file__))
	proj_path = os.path.abspath(os.path.join(model_path, os.pardir))
	goodbooks_path = os.path.join(proj_path, 'data/goodbooks')
	book2tag_path = os.path.join(goodbooks_path, 'book_tags.csv')
	book_data_path = os.path.join(goodbooks_path, 'books.csv')

	out_json = top_recommended_books(tweet_labels=tweet_labels,
									 book2tag_path=book2tag_path,
									 book_data_path=book_data_path,
									 )