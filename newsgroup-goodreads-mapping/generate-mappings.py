#!/usr/bin/python
import csv

# Read tags.csv
with open('tags.csv', 'r', encoding='utf8') as f:
	reader = csv.reader(f)
	tags = list(reader)

# Read book_tags.csv
with open('book_tags.csv', 'r', encoding='utf8') as f:
	reader = csv.reader(f)
	book_tags = list(reader)

# Newsgroup
newsgroups = [
	'atheism',
	'graphics',
	'computer',
	'computer',
	'computer',
	'computer',
	'sale',
	'automobile',
	'motor',
	'baseball',
	'hockey',
	'crypt',
	'electronic',
	'medical',
	'space',
	'christian',
	'guns',
	'mideast',
	'politics',
	'religion'
]

# Mappings
mappings = []

# Iterate through each newsgroup
for i in range(newsgroups.__len__()):
	news = newsgroups[i]
	news_mappings_count = []
	# Iterate through tags to find tags that contains the newsgroup keyword
	for tag in tags:
		tag_string = str(tag[1])
		if(tag_string.__contains__(news)):
			tag_id = tag[0]
			tag_id_count = []
			# Iterate through book_tags to get count
			for book_tag in book_tags:
				if book_tag[1] == tag_id:
					tag_id_count.append(book_tag[2])
			news_mappings_count.append([tag_id, max(tag_id_count)])
	# mappings = mappings + news_mappings

# Write to file
# with open('mappings.txt', 'w') as f:
	# f.writelines(mappings)

print('Program completed!')