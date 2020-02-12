import pandas as pd
import json
import os
import deepmatcher as dm


def split(all_df, shuffle=False, ratio=0.8):
    num = all_df.shape[0]
    offset = int(num * ratio)
    if num == 0 or offset < 1:
        return [], all_df
    if shuffle:
        all_df.sample(frac=1).reset_index(drop=True)
    train = all_df.loc[:offset]
    validation = all_df.loc[offset:]
    train.to_csv('train.csv', sep=',')
    validation.to_csv('validation.csv', sep=',')
    return train, validation


def read_labeled_data(labeled_data_path):
    print('>>> Reading labeled data...\n')
    labeled_data = pd.read_csv(labeled_data_path, low_memory=False)
    return labeled_data


def parse_labeled_data(labeled_data):

    labeled_data['left_title'] = ''
    labeled_data['right_title'] = ''
    for index, row in labeled_data.iterrows():
        left_page_title = get_page_title(row['left_spec_id'])
        right_page_title = get_page_title(row['right_spec_id'])
        labeled_data.at[index, 'left_title'] = left_page_title
        labeled_data.at[index, 'right_title'] = right_page_title

    labeled_data = labeled_data[['left_title', 'right_title', 'label']]
    return labeled_data


def get_page_title(spec_id):

    [website, id] = spec_id.split('//')
    id += '.json'
    data_path = os.path.join(dataset_path, website, id)
    with open(data_path) as f:
        page_title = json.load(f).get('<page title>').lower()
    return page_title


labeled_data_path = './modified_small_dataset.csv'
dataset_path = './2013_camera_specs'
output_path = './output'

labeled_data = read_labeled_data(labeled_data_path)
parsed_data = parse_labeled_data(labeled_data)
split(parsed_data)

train, validation = dm.data.process(
    path='',
    train='train.csv',
    validation='validation.csv')

model = dm.MatchingModel()
model.run_train(train, validation, best_save_path='best_model.pth')
