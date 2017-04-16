from inverted_index import Inverted_index
import os
import re
import time
import pickle
import math
from collections import Counter


def tf_idf_rank_list(term, index):
    # returns a sorted list of tf-idf score of a term in the query vector
    # format: [ ['doc1', w0], ['doc2', w1], .. ] where w0 > w1

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
    # return a list of queries with their serial numbers

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
    base_dir = "/home/nilesh/Documents/6th Semester/IR/en.docs.2011"
    count = 0
    query_location = '/home/nilesh/Documents/6th Semester/IR/' \
                     'Information-Retrieval-Lab-Components-.git/Evaluation/en.topics.126-175.2011.xml'

    try:
        file = open("Postinglist", 'rb', buffering=1)
        list1 = pickle.load(file)
        print("Index Loaded Successfully!!")
        print("Size of the Index: {}".format(len(list1)))
        print("Time taken : " + str(time.time() - start) + " seconds")

        query_list = read_queries(query_location)
        outputFile = open("sample_run.txt", "w")

        for query_element in query_list:
            query = query_element[1]
            query = pipe.remove_punctuations(query)
            query = pipe.stem(query)
            query = pipe.remove_stop_words(query)
            c = Counter()
            for term in query:
                c+= tf_idf_rank_list(term, list1)

            for x in range(0, len(query)):
                outputFile.write(str(126 + k) + " ")
                outputFile.write("Q0" + " ")
                outputFile.write(str(query[x][1]) + " ")
                outputFile.write(str(x + 1) + " ")
                outputFile.write(str(query[x][0]) + " ")
                outputFile.write("\n")
            outputFile.close()

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


        savedPickle = open("Postinglist", 'wb', buffering=1)
        pickle.dump(index, savedPickle, pickle.HIGHEST_PROTOCOL)
        print("Index created!")
        print("Size of Index: {}".format(len(Index)))
        print("Time taken : " + str(time.time() - start) + " seconds")
