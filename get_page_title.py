import pandas as pd
import os
import json

dataset_path = './2013_camera_specs'
output_path = './page_title'
columns_df = ['id', '<page title>']

for website in os.listdir(dataset_path):
    data = {'id': [], '<page title>': []}
    website_path = dataset_path + '/' + website
    print(website)
    fileList = os.listdir(website_path)
    for file in fileList:
        [num, form] = file.split('.')
        file = website_path + '/' + file
        f = open(file)
        attributes = json.load(f)
        for attribute in attributes:
            if attribute in data:
                data[attribute].append(attributes.get(attribute))
                break
    df = pd.DataFrame(data, columns=columns_df)
    save_path = output_path + '/' + website + '.csv'
    df.to_csv(save_path, index=False)

