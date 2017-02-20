'''
Created By: Nilesh Chaturvedi
Last Updated: 12th Feb, 2016
'''
import io
import os
import re
import string
import pickle
import time

suffixes = {
	    1: ["ो", "े", "ू", "ु", "ी", "ि", "ा"],
	    2: ["कर", "ाओ", "िए", "ाई", "ाए", "ने", "नी", "ना", "ते", "ीं", "ती", "ता", "ाँ", "ां", "ों", "ें"],
	    3: ["ाकर", "ाइए", "ाईं", "ाया", "ेगी", "ेगा", "ोगी", "ोगे", "ाने", "ाना", "ाते", "ाती", "ाता", "तीं", "ाओं", "ाएं", "ुओं", "ुएं", "ुआं"],
	    4: ["ाएगी", "ाएगा", "ाओगी", "ाओगे", "एंगी", "ेंगी", "एंगे", "ेंगे", "ूंगी", "ूंगा", "ातीं", "नाओं", "नाएं", "ताओं", "ताएं", "ियाँ", "ियों", "ियां"],
	    5: ["ाएंगी", "ाएंगे", "ाऊंगी", "ाऊंगा", "ाइयाँ", "ाइयों", "ाइयां"],
		}

class index():
	def __init__(self):
		self.postingList = {}
		self.document = []

	def stem(self, word):
		'''
		Obtains root word out of the unstemmed words.
		'''
		for L in 5, 4, 3, 2, 1:
			if (len(word) > L + 1):
				for suf in suffixes[L]:
					if word.endswith(suf):
						return word[:-L]
		return self.remove_punctuations(word)

	def remove_stop_words(self, document):
		'''
		Removes all the unnecessary frequently occouring stop words.
		'''
		stopWordList = open('stop_words.txt', 'r', buffering = 1).read().split()
		nlist = []
		for i in document:
			if i.strip() not in stopWordList:
				nlist.append(i)
		return nlist 

	def remove_punctuations(self, word):
		punctuationsList = list(string.punctuation)
		word = "".join(punct for punct in word if punct not in punctuationsList)
		return word

	def create_index(self, wordList, documentName):
		'''
		Uses dictionary to create Posting list of the documents.
		'''
		for newWord in wordList:
			if(len(self.postingList)!=0):
				if newWord in self.postingList.keys():
					self.postingList[newWord].append(documentName)
				else:
					self.postingList[newWord] = [documentName]
			else:
				self.postingList[newWord] = [documentName]
		return self.postingList

