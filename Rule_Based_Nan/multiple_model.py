import os
import csv
import pandas as pd

dataset_path = './model'
columns_df = ['id', '<page title>']
for brand in os.listdir(dataset_path):
    brand_path = dataset_path + '/' + brand
    fileList = os.listdir(brand_path)
    vis = {}
    ban_list = {}
    for file in fileList:
        if file == 'others.csv':
            continue
        file = brand_path + '/' + file
        with open(file, 'r', encoding='UTF-8') as f:
            reader = csv.reader(f)
            i = False
            for row in reader:
                if i:
                    if row[0] not in vis:
                        vis[row[0]] = 0
                    vis[row[0]] += 1
                if not i:
                    i = True
    for candidate in vis:
        if vis[candidate] > 3:
            ban_list[candidate] = 1
    if len(ban_list) != 0:
        for file in fileList:
            if file == 'others.csv':
                continue
            file = brand_path + '/' + file
            data = {'id': [], '<page title>': []}
            with open(file, 'r', encoding='UTF-8') as f:
                reader = csv.reader(f)
                i = False
                for row in reader:
                    if i:
                        if row[0] not in ban_list:
                            data['id'].append(row[0])
                            data['<page title>'].append(row[1])
                    if not i:
                        i = True
            df = pd.DataFrame(data, columns=columns_df)
            df.to_csv(file, index=False)
