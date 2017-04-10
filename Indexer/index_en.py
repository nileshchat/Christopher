from inverted_index import Inverted_index
import os
import re
import time
import pickle

start = time.time()
postingListDict = Inverted_index()
base_dir = "/home/nilesh/Documents/6th Semester/IR/en.docs.2011"
count = 0
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

savedPickle = open("Postinglist", 'wb', buffering=1)
pickle.dump(index, savedPickle, pickle.HIGHEST_PROTOCOL)
print("Posting List created!")
print("Size of Index: {}".format(len(index)))
print("Time taken : " + str(time.time() - start) + " seconds")

def dot_product(document_vector, query_vector):
    return 0