from merge import *

dataset_path = './model/Sony'

fileList = os.listdir(dataset_path)
ban_list = {'and 18': 1, 'b 16': 1, 'class 10': 1, 'digital 20': 1, 'e 18': 1, 'f1': 1, 'f2': 1, 'f3': 1, 'p1': 1,
            'pz 16': 1, 'sony 16': 1, 'sony18': 1,'v1':1}

print("Cleaning... Sony")
for file in fileList:
    [model, forma] = file.split('.')
    if model.lower() in ban_list:
        os.remove(dataset_path+'/'+file)


