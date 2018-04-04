#!/usr/bin/python
import sys

def get_mappings(filename, query_string, query_type):
	# Load file
	with open(filename, 'r') as f:
		mapping = f.readlines()
	mapping = [x.strip().split(' ') for x in mapping]

	# Specify query type
	if query_type == 'news':
		query_index = 0
		retrieve_index = 1
	elif query_type == 'books':
		query_index = 1
		retrieve_index = 0
	else:
		return []

	# Get result
	result = []
	for m in mapping:
		if m[query_index] == query_string:
			result.append(m[retrieve_index])

	# Return result
	return result

if __name__ == "__main__":

	# Example Usage (w/o command line arguments):
	# mappings_file_name = 'mappings.txt'
	# query_string = 'alt.atheism'
	# query_type = 'news'
	# result = getMappings(mappings_file_name, query_string, query_type)

	# Get command line arguments
	args = sys.argv

	# Get mappings
	if args.__len__() == 4:
		result = get_mappings(args[1], args[2], args[3])
		print(result)
	else:
		print("usage: news2books.py <mappings_file_name> <query_string> <query_type>")
		print("example: news2books.py mappings.txt alt.atheism news")