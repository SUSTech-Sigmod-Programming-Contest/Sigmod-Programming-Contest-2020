import os
from merge import *
dataset_path = './model/Sigma'

fileList = os.listdir(dataset_path)


print("Cleaning... Sigma")
for file in fileList:
    [model, forma] = file.split('.')
    if model[0:2] != 'DP' and model[0:2] !='SD':
        os.remove(dataset_path+'/'+file)