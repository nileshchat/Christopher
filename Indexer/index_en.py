from inverted_index import Inverted_index
import os
import re
import time
import pickle
import math

def dot_product(document_vector, query_vector):
# returns the dot product of 2 vectors

    return sum([Q*D for Q, D in zip(document_vector, query_vector)])

def modulus(vector):
# returns modulus of a vector
    mod = 0
    for component in vector:
        mod += component ** 2

    return math.sqrt(mod)

def read_queries(filename):
# return a list of queries with their serial numbers

    list = open(filename, 'r').readlines()
    new_list = []
    start = 126 #here we know the query number from where the queries start. At the moment this is hardcoded for convenience
    for word in list:
        if word.startswith("<title>"):
            entry = []
            query = word[7:(len(word) - 9)]
            entry.append(start)
            entry.append(query)
            new_list.append(entry)
            start += 1

    return new_list

start = time.time()
postingListDict = Inverted_index()
base_dir = "/home/nilesh/Documents/6th Semester/IR/en.docs.2011"
count = 0
query_location = '/home/nilesh/Documents/6th Semester/IR/' \
             'Information-Retrieval-Lab-Components-.git/Evaluation/en.topics.126-175.2011.xml'
for root, folders, file in os.walk(base_dir):
    for document in file:
        document_path = os.path.join(root+"/"+document)
        doc = re.sub('<[^<]+>',"", open(document_path, 'r', buffering = 1).read())
        #-------------------------------------------------------------------------
        # Standard Pipeline

        punctuated = postingListDict.remove_punctuations(doc)
        stemmed = postingListDict.stem(punctuated)
        chopped_stopwords = postingListDict.remove_stop_words(stemmed)
        #-------------------------------------------------------------------------
        # Update Index

        index = postingListDict.create_index(chopped_stopwords, document)
        print(count)
        count+=1

query_list = read_queries(query_location)

for query_element in query_list:
    query = query_element[1]

    for word in query:
        posting_list = postingListDict[word]

savedPickle = open("Postinglist", 'wb', buffering=1)
pickle.dump(index, savedPickle, pickle.HIGHEST_PROTOCOL)
print("Posting List created!")
print("Size of Index: {}".format(len(index)))
print("Time taken : " + str(time.time() - start) + " seconds")


