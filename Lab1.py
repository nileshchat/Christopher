import sys

uniset = list()  # Declare a universal set which would contain the set of words of every document

for i in sys.argv[1:]:
	uniset.append(set(open(i, 'r').read().split()))

def distinct(*params):
	for i in range(0, (len(uniset)-1)):
		while params not in uniset:
			out=params-uniset[i]
	return out

print (distinct(uniset[1]))
# file1 = open('doc_1.txt', 'r').read()
# file2 = open('doc_2.txt', 'r').read()
# file3 = open('doc_3.txt', 'r').read()

# s1=set(file1.split())
# s2=set(file2.split())
# s3=set(file3.split())

# dist_s1 = s1-s2-s3
# dist_s2 = s2-s1-s3
# dist_s3 = s3-s2-s1

# print len(dist_s1)
# print len(dist_s2)
# print len(dist_s3)