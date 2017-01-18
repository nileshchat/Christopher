import sys
import io

def distinct(params): #Returns a dictionary of words and frequency
		s1 = set(params)
		doc_dict = {}
		for i in s1:
			doc_dict[i] = params.count(i)
		
		return doc_dict


uniset = list()  # Declare a universal set which would contain the set of words of every document
unidict = {}	 # Declare a universal dictionary of all the distinct words of all the documents.

if len(sys.argv)<2:
	print ("Usage: Lab1.py -r filename1.txt filename 2.txt ....")

elif len(sys.argv)<3 and sys.argv[1] =='-r':
	print ('Usage: python3 Lab1.py [OPTIONS] FILENAME [FILENAME...] \n \nError: There needs to be atleast one document')
	print ('type python3 Lab1.py --help to see a list of available options.')

elif len(sys.argv)<3 and (sys.argv[1] =='--help' or '-h'):
	print ('Usage: python3 Lab1.py [OPTIONS] FILENAME [FILENAME...] \n \nOptions:')
	print ('{:4} {:9} {:11}'.format('', '-r', 'Get the list of words with their frequencies in the documents'))
	print ('{:4} {:9} {:11}'.format('', '-h --help', 'Get the available list of options'))

elif len(sys.argv)>3 and sys.argv[1] =='-r':
	for i in sys.argv[2:]:
		uniset.append(open(i, 'r').read().split())

	for i in uniset:

		print (distinct(i))
