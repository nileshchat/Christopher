import os
import re
from porter2stemmer import Porter2Stemmer
import string

base_dir = os.getcwd()
foldername = "en_test"
stemmed_l = []

for document in os.listdir(os.path.join(base_dir, foldername)):

    # Here .split() does the tokenization task
    doc = re.sub('<[^<]+>',"", open(base_dir+"/"+ foldername +"/{}".format(document), 'r', buffering = 1).read())
    ts = str.maketrans('','', string.punctuation)
    punctuated = (doc.translate(ts)).split()
    #perform operation
    stemmer = Porter2Stemmer()
    for word in punctuated:
        stemmed = stemmer.stem(word.lower())
        stemmed_l.append(stemmed)

    print(stemmed_l)