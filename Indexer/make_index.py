from index import index
import io
import os
import re
import pickle
import time

if __name__ == "__main__":

	start = time.time()
	basedir = os.getcwd() # Directory where the corpus is present
	folderName = "corpus" # Folder where all the documents are present
	postingListDict = index()

	term_frequency = {}

	try:
		file = open("Postinglist", 'rb', buffering = 1)
		list1 = pickle.load(file)
		for i in list1:
			print(i+":"+str(list1[i]))
		print("Size of the posting list: {}".format(len(list1)))
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

		'''
		Save Postinglist object file, so that the code does not have to create the Posting list again,
		can directly load the object for subsequent executions instead.
		'''
		savedPickle = open("Postinglist", 'wb', buffering = 1)
		pickle.dump(postingDictionary, savedPickle, pickle.HIGHEST_PROTOCOL)
		print("Posting List created!")
		print("Size of the posting list: {}".format(len(postingDictionary)))
		print("Time taken : "+str(time.time()-start)+" seconds")