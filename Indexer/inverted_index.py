from porter2stemmer import Porter2Stemmer
import string

#Create a list of stop words

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
    # returns a list of stemmed words

        stemmed_list = []
        stemmer = Porter2Stemmer()

        for word in list_of_words:
            stemmed_word = stemmer.stem(word.lower())
            stemmed_list.append(stemmed_word)

        return stemmed_list

    def remove_punctuations(self, sentence_string):
    #returns a list of words with punctuations removed in them

        translator = str.maketrans('', '', string.punctuation)

        return (sentence_string.translate(translator)).split()

    def remove_stop_words(self, tokenized_document):
    # returns a list with all the stop words removed

        without_stop_words = []

        for word in tokenized_document:
            if word not in stop_word_list:
                without_stop_words.append(word)

        return without_stop_words

    def create_index(self, document, document_name):
    #returns index
        unique_words = list(set(document))

        for newWord in unique_words:
            term_frequency = document.count(newWord)
            if (len(self.postingList) != 0):
                if newWord in self.postingList.keys():
                    doc_freq_tup = tuple([document_name, term_frequency])
                    self.postingList[newWord].append(doc_freq_tup)
                else:
                    doc_freq_tup = tuple([document_name, term_frequency])
                    self.postingList[newWord] = []
                    self.postingList[newWord].append(doc_freq_tup)
            else:
                doc_freq_tup = tuple([document_name, term_frequency])
                self.postingList[newWord] = []
                self.postingList[newWord].append(doc_freq_tup)

        return self.postingList


        