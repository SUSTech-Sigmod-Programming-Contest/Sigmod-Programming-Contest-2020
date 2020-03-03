import os
from merge import *
dataset_path = './model/Hikvision'

fileList = os.listdir(dataset_path)


def lack_hyphen(model):
    for alphabet in model:
        if alphabet == '-':
            return False
    return True


print("Cleaning... Hikvision")
for file in fileList:
    [model, forma] = file.split('.')
    if (lack_hyphen(model) or model[0] == 'I') and model != 'others':
        os.remove(dataset_path+'/'+file)
