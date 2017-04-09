#!/usr/bin/python
# import os
# import subprocess
# print("start")
# subprocess.call("./readAllFile.sh", shell=True)
# # print(rc.path)
# print(os.getenv('foo'))
# print("end")
import sys
import os
import glob
# from nltk import PorterStemmer
from porter2stemmer import Porter2Stemmer
import collections
import string
import pickle
import math
import re

class english_Index():
	def __init__(self):
		f = open("path.txt","r").read()
		path = (f.split())
		# print(path)
		self.flag = 0
		self.fileName = []
		for i in range(0,len(path)):
			p = path[i] + "/"
			# print(p)
			# print(os.path.isdir(p))
			if(os.path.isdir(p) == True):
				for file in os.listdir(p):
					self.fileName.append(p + file)
			else:
				print("english Corpus not Present in the folder")
				break

		# print(len(self.fileName))
		# print(self.fileName)


	def start(self):
		# print("start")
		self.english_dict = {}
		N = len(self.fileName)
		print("Reading File.....")
		for i in range(0,N):
			# print(self.fileName[i])
			if(i%500 == 0):
				print(i)
			f= open(self.fileName[i],'r').read()
			#read the content of file like substring between tag title
			# print(f)
			self.text1 = ""
			self.text2 = ""
			if(f.find('<DOCNO>') != -1):
				start = f.find('<DOCNO>')+len('<DOCNO>')
				end = f.find('</DOCNO')
				self.doc_id = f[start:end]
			# print(self.doc_id)
			if(f.find('<TITLE>') != -1):
				start = f.find('<TITLE>')+len('<TITLE>')
				end = f.find('</TITLE')
				self.text1 = f[start:end]
			#read the content of file like substring between tag content
			if(f.find('<TEXT>') != -1):
				start = f.find('<TEXT>')+len('<TEXT>')
				end = f.find('</TEXT')
				self.text2 = f[start:end]
			text = self.text1 + self.text2
			# print(text)
			text = self.remove_punctuation(text)
			text2 = self.remove_stopWord(text)
			text2 = self.stemming(text2)
			self.makePostingList(text2)	
		# print(self.english_dict['door'])

	def remove_punctuation(self, text):
		# print("remove")
		self.exclude = list(string.punctuation)
		text = "".join(c for c in text if c not in self.exclude)
		return text

	def remove_stopWord(self,text):
		# print("stopWord")
		stopWord=open("stop_eng.txt", "r").read().split("\n")
		# print(stopWord)
		text1 = []
		text = text.split()
		# print(text)
		for c in text:
			if c not in stopWord:
				text1.append(c)
		return text1

	def stemming(self,text):
		# print("stemming")
		s = Porter2Stemmer()
		root = []
		for w in text:
			root.append(s.stem(w))
		return root

	def makePostingList(self,text):
		# print("posting")
		l = set(text)
		wordUnique = list(l)
		for i in range(len(wordUnique)):
			c=text.count(str(wordUnique[i]))
			#make condition that if word present in another document then append the current document at that place otherwise make another row and store it there
			if self.flag != 0:
				if wordUnique[i] in self.english_dict.keys():
					self.english_dict[str(wordUnique[i])][self.doc_id] = c

				else:
					self.english_dict[str(wordUnique[i])] = {}
					self.english_dict[str(wordUnique[i])][self.doc_id] = c

			else:
				self.english_dict[str(wordUnique[i])] = {}
				self.english_dict[str(wordUnique[i])][self.doc_id] = 1
				self.flag = 1

	def getLength(self,doc):
		f = open(doc,"r").read()
		if(f.find('<TITLE>') != -1):
			start = f.find('<TITLE>')+len('<TITLE>')
			end = f.find('</TITLE')
			self.text1 = f[start:end]
			#read the content of file like substring between tag content
		if(f.find('<TEXT>') != -1):
			start = f.find('<TEXT>')+len('<TEXT>')
			end = f.find('</TEXT')
			self.text2 = f[start:end]
		text = self.text1 + self.text2
		return len(text)

	def dotProduct(self, Qvector, Dvector):
		# print(Qvector, Dvector)
		dotProduct = sum([x*y for x,y in zip(Qvector,Dvector)])
		# print(dotProduct)
		return dotProduct

	def squarRoot(self,w):
		sqSum = 0
		for sd in w:
			sqSum = sqSum + sd * sd
		# print(sqSum)
		return math.sqrt(sqSum)


if __name__ == "__main__":
	if os.path.isfile("path.txt") != True:
		path = []
		f = open("path.txt","w")
		t = 0
		for i in sys.argv:
			# print(i.find("IR"))
			if(t!=0):
				f.write(".." + i[32:]+ "\n")
			t=1
		f.close()
	else:
		# path = []
		if os.path.isfile("englishIndex.p") != True:
			obj = english_Index()
			if(os.path.isdir("../en.docs.2011/en_BDNews24/1") == True):
				obj.start()
			pickle.dump(obj.english_dict,open( "englishIndex.p", "wb" ))

		obj = english_Index()
		english_dict = {}
		english_dict = pickle.load(open("englishIndex.p", "rb" ))
		# print(english_dict)
		# print(len(english_dict))

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Reading query
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
		print("Reading Query")
		f1 = open("en.topics.126-175.2011.txt","r").read()
		# startNum = [x.start()+len("<num>") for x in re.finditer("\<num>",f)]
		# endNum = [x.start() for x in re.finditer("\</num>",f)]
		starTitle = [x.start()+len("<title>") for x in re.finditer("\<title>",f1)]
		endTitle = [x.start() for x in re.finditer("\</title>",f1)]
		starDesc = [x.start()+len("<desc>") for x in re.finditer("\<desc>",f1)]
		endDesc = [x.start() for x in re.finditer("\</desc>",f1)]
		# starTitle = [x.start()+len("<title>") for x in re.finditer("\<title>",f)]
		# endTitle = [x.start() for x in re.finditer("\</title>",f)]
		# id = [f[o:p] for o,p in zip(startNum,endNum)]
		# print(id)
		title = [f1[o:p] for o,p in zip(starTitle,endTitle)]
		# f1.close()
		desc = [f1[o:p] for o,p in zip(starDesc,endDesc)]
		Query = [o+" "+p for o,p in zip(title,desc)]
		# print(Query)
		# # print(title)


		# title = input("enter your query\n")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Query processed
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

		k=-1
		outputFile = open("sample_run.txt", "w")
		for n in Query:
			query = n
			k=k+1
			print(k)
			query = obj.remove_punctuation(query)
			query = obj.remove_stopWord(query)
			# print(query)
			query1 = set(query)
			query1 = list(query)
			length = len(query1)
			# print(obj.stemming(query1))
			docVector = collections.defaultdict(lambda: [0] * length)
			queryVector = [0]*length
			N = len(obj.fileName)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Create Query Vector
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

			for q in range(0,len(query1)):
				Qtf = query.count(query1[q])
				idf = math.log(N/(len(query1)))
				queryVector[q] = Qtf * idf
			# queryVector.insert(q,Qtf)
			sumQvector = sum([x for x in queryVector])
			# print(queryVector)
			queryVector = [(x)/sumQvector for x in queryVector]
			# print(queryVector)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Create Document Vector
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
			query = obj.stemming(query)
			j = 0
			for i in query:
				OccuresDocument = english_dict[i]
				df = len(OccuresDocument)
				idf = math.log(N/df)
				# flag =0
				for o in OccuresDocument.keys():
					tf = english_dict[i][o]
					w = (tf)*(idf)
					# queryLenght.insert(i,w)
					docVector[o][j] = w
				j = j+1
			# docVec = sorted(docVector.items())
			# print(docVector)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Doing the Normalization
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

			for doc, weight in docVector.items():
				#print(obj.fileName[doc-1])
				# docLength = obj.getLength(doc)
				# print(weight)
				squaroot = obj.squarRoot(weight)
				# print(docLength)
				# print(squaroot)
				for i in range(0,len(weight)):
				# 	#print("hello")	
				# 	# print((docVector[doc][i]))
				 	docVector[doc][i] = (docVector[doc][i])/(squaroot)
				 	# /(docLength)
			# print(docVector)
			# print(docVector["1060806_nation_story_6575492.utf8"])

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Calculate Dot product
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

			Scores=[[]]
			Scores=[ [obj.dotProduct(DocVec, queryVector), doc] for doc, DocVec in docVector.items() ]
			# print(Scores)
			Scores.sort(reverse = True)
			# print(Scores)
			# for x in Scores:
			# 	print(x[1])
			# print(Scores)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Write In the File
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
			print(126+k)
			for x in range(0,len(Scores)):
				outputFile.write(str(126+k) + " ")
				outputFile.write("Q0" + " ")
				outputFile.write(str(Scores[x][1]) + " ")
				outputFile.write(str(x + 1) + " ")
				outputFile.write(str(Scores[x][0]) + " ")
				outputFile.write("\n")
		outputFile.close()