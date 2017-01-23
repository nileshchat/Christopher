import sys
import io
import stringProcessor as sp
class PostingEntry():
	word = ""
	pList = []

def distinct(params): #Returns a dictionary of words and frequency
	s1 = set(params)
	doc_dict = {}
	for i in s1:
		doc_dict[i] = params.count(i)
	
	return doc_dict


List = []
dictList = []

for i in sys.argv[1:]:
		List.append(open(i, 'r', buffering = 1).read().split())

for i in List:
	for j in i:
		i.append(sp.hi_stem(j))
		i.remove(j)
	List.append(sp.removeStopWords(i))
	List.remove(i)

for i in List:
	for j in i:
		print (j)


