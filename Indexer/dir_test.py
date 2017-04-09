import sys
import os

base_dir = os.getcwd()

for root, folders, file in os.walk(base_dir):
    print(root)
