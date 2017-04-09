import porter2stemmer as ps
import string

stop_word_list = []

wordlist = open('stopwords_en.txt', 'r').readlines()

for word in wordlist:
    stop_word = word[:(len(word)-1)]
    stop_word_list.append(str(stop_word))

class Inverted_index():
    def __init__(self):
        self.postingList = {}
        self.document = []

    def stem(self, list_of_words):
        stemmer = ps()
        stemmed = stemmer.stem(list_of_words)

        return stemmed
    def remove_punctuations(self, sentence_string):
        #returns a list of words with punctuations removed in them

        translator = str.maketrans('', '', string.punctuations)
        return (sentence_string.translate(translator)).split()
    def remove_stop_words(self, tokenized_document):
        # returns a list with all the stop words removed

        without_stop_words = []
        for word in tokenized_document:
            if word not in stop_word_list:
                without_stop_words.append(word)
        