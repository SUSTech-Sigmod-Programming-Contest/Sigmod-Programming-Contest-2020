from merge import *

dataset_path = './model/Canon'

fileList = os.listdir(dataset_path)
ban_list = {'4l': 1, '8f': 1, 'e1': 1, 'e3': 1, 'e7': 1, 'efs 18': 1, 'eos-1d': 1, 'is 24': 1, 'lens 18': 1,
            'lens 55': 1, 'quantaray 18': 1, 'f3': 1,
            's 18': 1, 's 55': 1, 'sigma 18': 1, 'sigma 70': 1, 'slr 10': 1, 'stm 18': 1, 'tamron 18': 1, 'v1': 1,
            'usm 75': 1,'DS 6041':1,'DS126191':1,'DS126311':1}

print("Cleaning... Canon")
for file in fileList:
    [model, forma] = file.split('.')
    if model.lower() in ban_list:
        os.remove(dataset_path + '/' + file)


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
        if len(b) > 3 and b[-2:].lower() == 'is':
            if test_prefix(a, b) and len(b) - len(a) == 2:
                print(a, b)
                merge(a, b, dataset_path, 1)

        if len(b) > 3 and b[-2:].lower() == 'hs':
            if test_prefix(a, b) and len(b) - len(a) == 2:
                print(a, b)
                merge(a, b, dataset_path, 1)
