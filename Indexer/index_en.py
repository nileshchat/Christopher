'''
Author: Nilesh Chaturvedi
Last Updated: 17th April, 2017
'''

import os
import re
import time
import pickle
import math
from collections import Counter
from inverted_index import Inverted_index

def tf_idf_rank_list(term, index):
    # Returns a sorted list of tf-idf score of a term in the query vector
    # Format: [ ['doc1', w0], ['doc2', w1], .. ] where w0 > w1

    retrieved_docs = {}
    posting_list = index[term]
    squared_weight_sum = 0

    DF = posting_list.keys()

    IDF = math.log(len(index) / len(DF))

    for doc in posting_list.keys():
        weight = posting_list[doc] * IDF
        squared_weight_sum += weight * weight
        retrieved_docs[doc] = weight

    # Cosine Normalization

    for doc in retrieved_docs.keys():
        retrieved_docs[doc] = retrieved_docs[doc] / math.sqrt(squared_weight_sum)

    return Counter(retrieved_docs)


def read_queries(filename):
    # Returns a list of queries with their serial numbers
    # Format : [[126, 'Random Query'], [127, 'Another Random Query'], ..]

    list = open(filename, 'r').readlines()
    new_list = []
    start = 126  # here we know the query number from where the queries start. At the moment this is hardcoded for convenience
    for word in list:
        if word.startswith("<title>"):
            entry = []
            query = word[7:(len(word) - 9)]
            entry.append(start)
            entry.append(query)
            new_list.append(entry)
            start += 1

    return new_list


if __name__ == "__main__":

    start = time.time()
    index = Inverted_index()
    pipe = Inverted_index()
    count = 0
    # Give the location where files to be indexed are there.
    base_dir = "/home/nilesh/Documents/6th Semester/IR/en.docs.2011"
    
    # Give the location of file which contains queries.
    query_location = '/home/nilesh/Documents/6th Semester/IR/' \
                     'Information-Retrieval-Lab-Components-.git/Evaluation/en.topics.126-175.2011.xml'

    # Case where The index has already been created.
    try:
        file = open("Index", 'rb', buffering=1)
        list1 = pickle.load(file)
        print("Index Loaded Successfully!!")
        print("Size of the Index: {}".format(len(list1)))
        print("Time taken to load the Index: " + str(time.time() - start) + " seconds")

        query_list = read_queries(query_location)
        outputFile = open("sample_run.txt", "w")
        flag = 126

        for query_element in query_list:
            query = query_element[1]
            query = pipe.remove_punctuations(query)
            query = pipe.stem(query)
            query = pipe.remove_stop_words(query)
            c = Counter()
            for term in query:
                c+= tf_idf_rank_list(term, list1)

            rank_list = c.most_common()

            for result in range(0,6):
                outputFile.write(str(flag) + " ")
                outputFile.write("Q0" + " ")
                outputFile.write(str(rank_list[result][0]) + " ")
                outputFile.write(str(result+1) + " ")
                outputFile.write(str(rank_list[result][1]) + "\n")
            flag += 1

        outputFile.close()

    # Case where the index needs to be created.
    except:
        print("Couldn't find an Index. Index Generation in progress. \nThis will take some significant time!!")
        for root, folders, file in os.walk(base_dir):
            for document in file:
                document_path = os.path.join(root + "/" + document)
                doc = re.sub('<[^<]+>', "", open(document_path, 'r', buffering=1).read())
                # -------------------------------------------------------------------------
                # Standard Pipeline

                punctuated = index.remove_punctuations(doc)
                stemmed = index.stem(punctuated)
                chopped_stopwords = index.remove_stop_words(stemmed)
                # -------------------------------------------------------------------------
                # Update Index

                Index = index.create_index(chopped_stopwords, document)
                print(count)
                count += 1


        savedPickle = open("Index", 'wb', buffering=1)
        pickle.dump(index, savedPickle, pickle.HIGHEST_PROTOCOL)
        print("Index created!")
        print("Size of Index: {}".format(len(Index)))
        print("Time taken : " + str(time.time() - start) + " seconds")
