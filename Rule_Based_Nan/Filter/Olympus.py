from merge import *

dataset_path = './model/Olympus'

fileList = os.listdir(dataset_path)
ban_list = {'e1': 1, 'f2': 1, 'ihs 12': 1, 'ihs 14': 1, 'olympus 14': 1, 'p1': 1, 'v2': 1}

print("Cleaning... Olympus")
for file in fileList:
    [model, forma] = file.split('.')
    if model.lower() in ban_list:
        os.remove(dataset_path+'/'+file)
