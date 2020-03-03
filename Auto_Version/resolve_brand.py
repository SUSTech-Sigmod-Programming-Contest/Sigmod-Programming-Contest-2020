import os
import csv
import pandas as pd

dataset_path = './model'
resolve_list = {}
columns_df = ['id', '<page title>']


def check(page_title, identifier):
    if page_title.lower().find(identifier) != -1 and page_title.lower().find(identifier) < len(page_title) / 2:
        return True
    return False


for brand in os.listdir(dataset_path):
    brand_path = dataset_path + '/' + brand
    fileList = os.listdir(brand_path)
    for file in fileList:
        total = 0
        cnt = 0
        score = 0
        file = brand_path + '/' + file
        with open(file, 'r', encoding='UTF-8') as f:
            reader = csv.reader(f)
            i = False
            for row in reader:
                if i:
                    total += 1
                    if check(row[1], ' i '):
                        cnt += 1
                        score |= 1
                    if check(row[1], ' ii '):
                        score |= 2
                        cnt += 1
                    if check(row[1], ' iii '):
                        cnt += 1
                        score |= 3
                if not i:
                    i = True
        if score == 3 and cnt > 0.25 * total:
            resolve_list[file] = 1

resolve_list['./model/Canon/7D.csv'] = 1

vis = {}
for file in resolve_list:
    with open(file, 'r', encoding='UTF-8') as f:
        pre = file[0:-4]
        print(pre)
        reader = csv.reader(f)
        data = {'id': [], '<page title>': []}
        data_ii = {'id': [], '<page title>': []}
        data_iii = {'id': [], '<page title>': []}
        data_iv = {'id': [], '<page title>': []}
        i = False
        for row in reader:
            if i:
                if row[1].lower().find(' ii ') != -1:
                    data_ii['id'].append(row[0])
                    data_ii['<page title>'].append(row[1])
                elif row[1].lower().find(' iii ') != -1:
                    data_iii['id'].append(row[0])
                    data_iii['<page title>'].append(row[1])
                elif row[1].lower().find(' iv ') != -1:
                    data_iv['id'].append(row[0])
                    data_iv['<page title>'].append(row[1])
                else:
                    data['id'].append(row[0])
                    data['<page title>'].append(row[1])
            if not i:
                i = True
        df = pd.DataFrame(data, columns=columns_df)
        df.to_csv(pre + '.csv', index=False)

        df = pd.DataFrame(data_ii, columns=columns_df)
        df.to_csv(pre + ' II.csv', index=False)

        df = pd.DataFrame(data_iii, columns=columns_df)
        df.to_csv(pre + ' III.csv', index=False)

        df = pd.DataFrame(data_iv, columns=columns_df)
        df.to_csv(pre + ' IV.csv', index=False)

