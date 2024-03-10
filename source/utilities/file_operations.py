# a function that loads file, takes as input the file path and returns the file content

import os

def load(filename):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, '..',filename)
    with open(file_path, 'r') as file:
        return file.read()

#create directory "downloaded_jsons" if it doesnt exuist and save the json file
def save(json, filename):
    current_dir = os.path.dirname(__file__)
    if not os.path.exists(os.path.join(current_dir, '..', 'downloaded_jsons')):
        os.makedirs(os.path.join(current_dir, '..', 'downloaded_jsons'))
    file_path = os.path.join(current_dir, '..', 'downloaded_jsons',filename)
    with open(file_path, 'w') as file:
        file.write(json)
