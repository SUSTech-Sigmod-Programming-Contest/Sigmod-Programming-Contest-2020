from merge import *

dataset_path = './model/Canon'

fileList = os.listdir(dataset_path)
ban_list = {'4l': 1, '8f': 1, 'e1': 1, 'e3': 1, 'e7': 1, 'efs 18': 1, 'eos-1d': 1, 'is 24': 1, 'lens 18': 1,
            'lens 55': 1, 'quantaray 18': 1, 'f3': 1,
            's 18': 1, 's 55': 1, 'sigma 18': 1, 'sigma 70': 1, 'slr 10': 1, 'stm 18': 1, 'tamron 18': 1, 'v1': 1,
            'usm 75': 1}

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
                merge(a, b, dataset_path)
        if len(b) > 3 and b[-2:].lower() == 'hs':
            if test_prefix(a, b) and len(b) - len(a) == 2:
                print(a, b)
                merge(a, b, dataset_path)

merge('500D', 'T1i', dataset_path)
merge('550D', 'T2i', dataset_path)
merge('600D', 'T3i', dataset_path)
merge('650D', 'T4i', dataset_path)
merge('700D', 'T5i', dataset_path)
merge('1100D', 'T3', dataset_path)
merge('1200D', 'T5', dataset_path)
merge('xs', 'XS 10', dataset_path)
merge('xsi', 'XSi 12', dataset_path)
merge('xti', 'XTi 10', dataset_path)

merge('SD200', 'IXUS 30', dataset_path)
merge('SD300', 'IXUS 40', dataset_path)
merge('SD400', 'IXUS 50', dataset_path)
merge('SD450', 'IXUS 55', dataset_path)
merge('SD600', 'IXUS 60', dataset_path)
merge('SD 630', 'IXUS 65', dataset_path)

merge('SD1000', 'IXUS 70', dataset_path)
merge('SD750', 'IXUS 75', dataset_path)
merge('SD1100', 'IXUS 80', dataset_path)
merge('SD790', 'IXUS 90', dataset_path)
merge('SD1200', 'IXUS 95', dataset_path)
merge('SD780', 'IXUS 100', dataset_path)
merge('SD1300', 'IXUS 105', dataset_path)
merge('SD960', 'IXUS 110', dataset_path)
merge('SD1400', 'IXUS 130', dataset_path)
merge('SD980', 'IXUS 200', dataset_path)
merge('SD3500', 'IXUS 210', dataset_path)
merge('SD4000', 'IXUS 300', dataset_path)
merge('SD550', 'IXUS 750', dataset_path)
merge('SD700', 'IXUS 800', dataset_path)
merge('SD800', 'IXUS 850', dataset_path)
merge('SD870', 'IXUS 860', dataset_path)
merge('SD880', 'IXUS 870', dataset_path)
merge('SD850', 'IXUS 950', dataset_path)
merge('sd 890', 'IXUS 970', dataset_path)

merge('Sd990', 'IXUS 980', dataset_path)
merge('SD4500', 'IXUS 1000', dataset_path)

merge('S400', 'IXUS 400', dataset_path)
merge('S410', 'IXUS 430', dataset_path)

merge('ELPH 100', 'IXUS 115', dataset_path)
merge('ELPH 110', 'IXUS 125', dataset_path)
merge('ELPH 300', 'IXUS 220', dataset_path)
merge('ELPH 310', 'IXUS 230', dataset_path)
merge('ELPH 500', 'IXUS 310', dataset_path)
merge('ELPH 520', 'IXUS 500', dataset_path)
