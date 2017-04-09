list = open('stopwords_en.txt', 'r').readlines()
new_list = []
for word in list:
    entry = word[:(len(word)-1)]
    new_list.append(str(entry))
print(new_list)