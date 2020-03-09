from merge import *

dataset_path = './model'
E = 2


def calculate_intersection(A, B):
    cnt = 0
    vis = {}
    with open(A, 'r', encoding='UTF-8') as file:
        reader = csv.reader(file)
        isNotFirstLine = False
        for row in reader:
            if isNotFirstLine:
                vis[row[0]] = 1
            else:
                isNotFirstLine = True
    with open(B, 'r', encoding='UTF-8') as file:
        reader = csv.reader(file)
        isNotFirstLine = False
        for row in reader:
            if isNotFirstLine:
                if row[0] in vis:
                    cnt += 1
            else:
                isNotFirstLine = True
    return cnt


for brand in os.listdir(dataset_path):
    print(brand)
    Flag = True
    while Flag:
        model_list = []
        remove_path = []
        Flag = False
        for model in os.listdir(dataset_path + '/' + brand):
            model_list.append(dataset_path + '/' + brand + '/' + model)
        for i in range(0, len(model_list)):
            for j in range(i + 1, len(model_list)):
                n = calculate_intersection(model_list[i], model_list[j])
                if n > E:
                    Flag = True
                    merge(model_list[i][:-4][8:], model_list[j][:-4][8:], './model', 0)
                    remove_path.append(model_list[j])
                    print(model_list[i][:-4][8:])
                    print(model_list[j][:-4][8:])
                    print()
        for path in remove_path:
            if os.path.exists(path):
                os.remove(path)
