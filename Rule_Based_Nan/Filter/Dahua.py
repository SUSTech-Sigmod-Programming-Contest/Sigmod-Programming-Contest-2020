import os

dataset_path = './model/Dahua'

fileList = os.listdir(dataset_path)


def contain_space(model):
    for alphabet in model:
        if alphabet == ' ':
            return True
    return False


print("Cleaning... Dahua")
for file in fileList:
    [model, forma] = file.split('.')
    if len(model) <= 4 or contain_space(model):
        os.remove(dataset_path+'/'+file)
