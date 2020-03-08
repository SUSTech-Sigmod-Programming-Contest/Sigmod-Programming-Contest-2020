import os
import csv
import pandas as pd
import preprocessing
from copy import *

page_title_list = copy(preprocessing.page_title)
E = 3

dataset_path = './model'
columns_df = ['left_spec_id', 'right_spec_id']
data = {'left_spec_id': [], 'right_spec_id': []}

for brand in os.listdir(dataset_path):
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

    for i in range(0, len(keys)):
        for j in range(i + 1, len(keys)):
            a = page_title_list[keys[i]]
            b = page_title_list[keys[j]]
            if a == b and len(a) > 10:
                data['left_spec_id'].append(keys[i])
                data['right_spec_id'].append(keys[j])

df = pd.DataFrame(data, columns=columns_df)
df.to_csv('./judge/duplicate.csv', index=False)