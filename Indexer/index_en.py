from inverted_index import Inverted_index
import os
import re
from porter2stemmer import Porter2Stemmer
import string

base_dir = os.getcwd()
foldername = "en_test"
postingListDict = Inverted_index()

for document in os.listdir(os.path.join(base_dir, foldername)):

    doc = re.sub('<[^<]+>',"", open(base_dir+"/"+ foldername +"/{}".format(document), 'r', buffering = 1).read())
    punctuated = postingListDict.remove_punctuations(doc)
    stemmed = postingListDict.stem(punctuated)
    chopped_stopwords = postingListDict.remove_stop_words(stemmed)
    index = postingListDict.create_index(chopped_stopwords, document)

    print(index)