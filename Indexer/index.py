'''
Created By: Nilesh Chaturvedi
Last Updated: 12th Feb, 2016

Description: This code takes in as input name of the folder which contains the text documents out of which the posting 
list is to be created.
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
		for L in 5, 4, 3, 2, 1:
			if (len(word) > L + 1):
				for suf in suffixes[L]:
					if word.endswith(suf):
						return word[:-L]
		return self.remove_punctuations(word)

	def remove_stop_words(self, document):
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
		for newWord in wordList:
			if(len(self.postingList)!=0):
				if newWord in self.postingList.keys():
					self.postingList[newWord].append(documentName)
				else:
					self.postingList[newWord] = [documentName]
			else:
				self.postingList[newWord] = [documentName]
		return self.postingList

if __name__ == "__main__":

	start = time.time()

	basedir = os.getcwd()
	folderName = "folder" 
	postingListDict = index()

	try:
		file = open("Postinglist", 'rb', buffering = 1)
		list1 = pickle.load(file)
		for i in list1:
			print(i+":"+str(list1[i]))
		print("Time taken : "+str(time.time()-start)+" seconds")	
	
	except:
		for document in os.listdir(basedir+"/"+folderName):
				doc=(re.sub('<[^<]+>',"", open(basedir+"/"+folderName+"/{}".format(document), 'r', buffering = 1).read())).split()
				#(open(basedir+"/"+folderName+"/{}".format(document)).read().split())
				#(re.sub('<[^<]+>',"", open(basedir+"/"+folderName+"/{}".format(i)).read())).split()

				for word in doc:
					stword = postingListDict.stem(word.strip())
					if (word != " "):
						doc.append(stword)
					doc.remove(word)
				newDoc = set(postingListDict.remove_stop_words(doc))
				postingDictionary = postingListDict.create_index(newDoc, document)

		savedPickle = open("Postinglist", 'wb' )
		pickle.dump(postingDictionary, savedPickle, pickle.HIGHEST_PROTOCOL)
		print("Posting List created!")
		print("Time taken : "+str(time.time()-start)+" seconds")