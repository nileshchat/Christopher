args=raw_input()
args_list=args.split()

files=len(args_list)
uniset = list()
for i in args_list:
	uniset.append(set(open(i, 'r').read().split()))


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