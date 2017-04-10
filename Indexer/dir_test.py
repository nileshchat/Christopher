import sys
import os

base_dir = "/home/nilesh/Documents/6th Semester/IR/en.docs.2011"
directory_list = []
for root, folders, file in os.walk(base_dir):
    for element in file:
        element = os.path.join(root+"/"+element)
        directory_list.append(element)
        print(element)
