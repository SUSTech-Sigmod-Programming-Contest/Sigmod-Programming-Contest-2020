import os
from find_page_title import *
from edit_distance import *
import pandas as pd
E = 3

dataset_path = './model'
columns_df = ['left_spec_id', 'right_spec_id']
data = {'left_spec_id': [], 'right_spec_id': []}
table = {}

with open('./page_title/page_title.csv', 'r', encoding='UTF-8') as file:
    reader = csv.reader(file)
    isNotFirstLine = False
    for row in reader:
        if isNotFirstLine:
            table[row[0]] = row[1]
        if not isNotFirstLine:
            isNotFirstLine = True

for brand in os.listdir(dataset_path):
    print(brand, end=": ")
    brand_path = dataset_path + '/' + brand
    fileList = os.listdir(brand_path)
    keys = []
    for file in fileList:
        if file != 'others.csv':
            continue
        file = brand_path + '/' + file
        with open(file, 'r', encoding='UTF-8') as f:
            reader = csv.reader(f)
            i = False
            for row in reader:
                if i:
                    keys.append(row[0])
                if not i:
                    i = True
    print(len(keys))

    for i in range(0, len(keys)):
        for j in range(i + 1, len(keys)):
            a = table[keys[i]]
            b = table[keys[j]]
            if a == b and len(a) > 10:
                print(keys[i],end=" ")
                print(a)
                print(keys[j],end=" ")
                print(b)
                print()
                data['left_spec_id'].append(keys[i])
                data['right_spec_id'].append(keys[j])

df = pd.DataFrame(data, columns=columns_df)
df.to_csv('./judge/duplicate.csv', index=False)