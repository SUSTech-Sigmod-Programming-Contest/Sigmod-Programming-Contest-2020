import pandas as pd
import os
import json


if __name__ == '__main__':
    dataset_path = './2013_camera_specs'
    output_path = './page_title'
    columns_df = ['id', '<page title>']
    data = {'id': [], '<page title>': []}
    for website in os.listdir(dataset_path):
        website_path = dataset_path + '/' + website
        print(website)
        fileList = os.listdir(website_path)
        for file in fileList:
            key = website + '//' + file[0:-5]
            file = website_path + '/' + file
            f = open(file)
            attributes = json.load(f)
            for attribute in attributes:
                if attribute == '<page title>':
                    data['id'].append(key)
                    data['<page title>'].append(attributes.get(attribute))
                    break
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    df = pd.DataFrame(data, columns=columns_df)
    save_path = output_path + '/' + 'page_title.csv'
    df.to_csv(save_path, index=False)
