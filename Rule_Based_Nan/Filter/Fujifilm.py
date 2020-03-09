from merge import *

dataset_path = './model/Fujifilm'

fileList = os.listdir(dataset_path)
ban_list = {'f1': 1, 'p1': 1, 'v1': 1}

print("Cleaning... Fujifilm")
for file in fileList:
    [model, forma] = file.split('.')
    if model.lower() in ban_list:
        os.remove(dataset_path+'/'+file)


def test_prefix(a, b):
    for k in range(0, len(a)):
        if a[k].lower() != b[k].lower():
            return False
    return True


for i in range(0, len(fileList)):
    for j in range(i + 1, len(fileList)):
        [a, forma] = fileList[i].split('.')
        [b, forma] = fileList[j].split('.')
        if len(a) > len(b):
            temp = a
            a = b
            b = temp
        if len(b) > 5 and b[-3:].lower() == 'exr':
            if test_prefix(a, b) and len(b)-len(a) == 3:
                print(a, b)
                merge(a, b, dataset_path,1)


        if len(b) > 5 and b[-5:].lower() == 'black':
            if test_prefix(a, b) and len(b)-len(a) == 5:
                print(a, b)
                merge(a, b, dataset_path,1)
