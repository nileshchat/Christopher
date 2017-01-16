import sys

uniset = list()  # Declare a universal set which would contain the set of words of every document
unidict = {}

for i in sys.argv[1:]:
	uniset.append(open(i, 'r').read().split())

def distinct(params): #Returns a dictionary of words and frequency
	s1 = set(params)
	doc_dict = {}
	for i in s1:
		doc_dict[i] = params.count(i)
	
	return doc_dict


def merge_dict(dict1, dict2): # Function to merge two dictionaries, so that excess load due to a huge dictionary of words of all the documents, can be avoided.
	for a, b in dict1.items():
		for c, d in dict2.items():
			if a==c:
				dict2[a]+=dict1[c]
				unidict[a] = dict2[a]
			else:
				unidict[c]=d
	return unidict
al = {'a': 20, 'cd': 12, 'abc':10}
bl = {'a':10, 'abc': 1, 'xx': 14}

print (merge_dict(al, bl))
