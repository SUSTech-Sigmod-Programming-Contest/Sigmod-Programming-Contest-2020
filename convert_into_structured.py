import pandas as pd
import json
import os

dataset_path = './2013_camera_specs'
website_path = ''
output_path = './structured_data'
fileList = ''
E = 0.8


def confirm_attributes():
    count = 0
    candidates = {}
    headers = []
    columns_df = ['id']
    for file in fileList:
        count += 1
        file = website_path + '/' + file
        f = open(file)
        attributes = json.load(f)
        for attribute in attributes:
            if attribute not in candidates:
                candidates[attribute] = 0
                headers.append(attribute)
            candidates[attribute] += 1

    candidates = sorted(candidates.items(), key=lambda x: -x[1])
    for candidate in candidates:
        [header, cnt] = candidate
        if cnt > count * E:
            columns_df.append(header)
    return columns_df


def create_dataframes(columns_df, save_path):
    data = {}
    for column in columns_df:
        data[column] = []
    for file in fileList:
        [num, form] = file.split('.')
        data['id'].append(num)
        vis = {'id': 1}
        file = website_path + '/' + file
        f = open(file)
        attributes = json.load(f)
        for attribute in attributes:
            if attribute in data:
                data[attribute].append(attributes.get(attribute))
                vis[attribute] = 1
        for column in columns_df:
            if column not in vis:
                data[column].append('X')
    df = pd.DataFrame(data, columns=columns_df)
    df.to_csv(output_path + save_path, index=False)
    return


if __name__ == '__main__':
    websites = [f for f in os.listdir(dataset_path)]
    for website in websites:
        website_path = dataset_path+'/'+website
        fileList = os.listdir(website_path)
        print(website_path)
        columns_df = confirm_attributes()
        print(columns_df)
        print()
        create_dataframes(columns_df, './'+website+'.csv') 

