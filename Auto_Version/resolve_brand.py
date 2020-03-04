import os
import csv
import pandas as pd
import re

dataset_path = './model'
resolve_list = {}
columns_df = ['id', '<page title>']


def word_index(string, word):
    index = 0
    for each_word in string.split(' '):
        if each_word == word:
            return index
        else:
            index = index + 1
    return -1


def check(page_title, identifier):
    if page_title.lower().find(identifier) == -1:
        return False
    words = page_title.lower().split(' ')
    for ith in range(2, len(words)):
        if words[ith] == identifier and \
                not re.match('[0-9]+$', words[ith-1]) and \
                not re.match('[0-9]+$', words[ith-2]):
            return True
    return False


def check_has(page_title, identifier):
    if page_title.lower().find(identifier) != -1 and \
            page_title.lower().find(identifier) < len(page_title) / 2:
        return True
    return False


for brand in os.listdir(dataset_path):
    brand_path = dataset_path + '/' + brand
    fileList = os.listdir(brand_path)
    for model_file in fileList:
        total = 0
        cnt = 0
        score = 0
        model, _ = model_file.lower().split('.')
        model_file = brand_path + '/' + model_file
        with open(model_file, 'r', encoding='UTF-8') as f:
            reader = csv.reader(f)
            i = False
            for row in reader:
                if i:
                    total += 1
                    if check_has(row[1], ' i '):
                        cnt += 1
                        score |= 1
                    if check_has(row[1], ' ii '):
                        score |= 2
                        cnt += 1
                    if check_has(row[1],  ' iii '):
                        cnt += 1
                        score |= 3
                if not i:
                    i = True
        if score == 3 and cnt > 0.25 * total:  # 如果某个品牌有I II III IV的数量大于一定值才考虑区分
            resolve_list[model_file] = 1

resolve_list['./model/Canon/7D.csv'] = 1

vis = {}
for model_file in resolve_list:
    with open(model_file, 'r', encoding='UTF-8') as f:
        pre = model_file[0:-4]
        reader = csv.reader(f)
        data = {'id': [], '<page title>': []}
        data_ii = {'id': [], '<page title>': []}
        data_iii = {'id': [], '<page title>': []}
        data_iv = {'id': [], '<page title>': []}
        i = False
        for row in reader:
            if i:
                if check(row[1], 'iii'):
                    data_iii['id'].append(row[0])
                    data_iii['<page title>'].append(row[1])
                elif check(row[1], 'ii'):
                    data_ii['id'].append(row[0])
                    data_ii['<page title>'].append(row[1])
                elif check(row[1], 'iv'):
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

