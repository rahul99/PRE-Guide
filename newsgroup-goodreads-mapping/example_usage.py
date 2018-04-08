import news2books

# For newsgroup to goodreads mapping 
newsgroup_id = '0'	
tag_ids = news2books.get_mappings('mappings.txt', newsgroup_id, 'news')
print('Mappings for newsgroup_id ' + newsgroup_id + ' is ' + str(tag_ids))

# For goodreads to newsgroup mapping
goodreads_id = '81'		
tweet_cat_ids = news2books.get_mappings('mappings.txt', goodreads_id, 'books')
print('Mappings for goodreads_id ' + goodreads_id + ' is ' + str(tweet_cat_ids))