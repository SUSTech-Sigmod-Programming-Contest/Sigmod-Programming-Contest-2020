from merge import *

dataset_path = './model/Pentax'

fileList = os.listdir(dataset_path)
ban_list = {'al 18': 1, 'da 18': 1, 'dal 18': 1, 'l 18': 1}

print("Cleaning... Pentax")
for file in fileList:
    [model, forma] = file.split('.')
    if model.lower() in ban_list:
        os.remove(dataset_path+'/'+file)