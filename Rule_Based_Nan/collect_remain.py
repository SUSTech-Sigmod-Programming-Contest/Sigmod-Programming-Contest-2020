import os
import csv
import pandas as pd

dataset_path = './model'
columns_df = ['id', '<page title>']

vis = {}


def collect_remain(website, file):
    data = {'id': [], '<page title>': []}
    with open(file, 'r', encoding='UTF-8') as f:
        reader = csv.reader(f)
        isNotFirstLine = False
        for row in reader:
            if isNotFirstLine:
                key = row[0]
                page_title = row[1]
                if key not in vis:
                    data['id'].append(key)
                    data['<page title>'].append(page_title)
            else:
                isNotFirstLine = True
    df = pd.DataFrame(data, columns=columns_df)
    df.to_csv(dataset_path + '/' + website + '/' + 'others.csv', index=False)


for website in os.listdir(dataset_path):
    website_path = dataset_path + '/' + website
    fileList = os.listdir(website_path)
    for file in fileList:
        file = website_path + '/' + file
        with open(file, 'r', encoding='UTF-8') as f:
            reader = csv.reader(f)
            i = False
            for row in reader:
                if i:
                    vis[row[0]] = 1
                if not i:
                    i = True

for website in os.listdir(dataset_path):
    website_path = dataset_path + '/' + website
    fileList = os.listdir(website_path)
    for file in fileList:
        file = website_path+'/'+file
        collect_remain(website, file)
