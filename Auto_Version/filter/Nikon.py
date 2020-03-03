from merge import *

dataset_path = './model/Nikon'

fileList = os.listdir(dataset_path)
ban_list = {'af 18': 1, 'af 70': 1, 'f1': 1, 'f3': 1, 'f4': 1, 'f5': 1, 'nikkor 18': 1, 'nikkor 35': 1, 'nikkor 55': 1,
            'nikon 16': 1, 'p1': 1, 'sigma 70': 1, 'u1': 1, 'v1': 1, 'v2': 1, 'vr10': 1,'y1':1}

print("Cleaning... Nikon")
for file in fileList:
    [model, forma] = file.split('.')
    if model.lower() in ban_list:
        os.remove(dataset_path+'/'+file)
