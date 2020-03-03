import os
from merge import *
dataset_path = './model/SVP'

fileList = os.listdir(dataset_path)


print("Cleaning... SVP")
for file in fileList:
    [model, forma] = file.split('.')
    if model[0:3] == '500':
        os.remove(dataset_path+'/'+file)