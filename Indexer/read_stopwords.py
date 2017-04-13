list = open('/home/nilesh/Documents/6th Semester/IR/'
            'Information-Retrieval-Lab-Components-.git/Evaluation/en.topics.126-175.2011.xml',
            'r').readlines()
new_list = []
start = 126
for word in list:
    if word.startswith("<title>"):
        entry = []
        query = word[7:(len(word)-9)]
        entry.append(start)
        entry.append(query)
        new_list.append(entry)
        start += 1