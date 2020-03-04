import pandas as pd
import json
import os
import deepmatcher as dm


def split(all_df, shuffle=False, traning_ratio=0.6, validation_ratio=0.2, test_ratio=0.2):
    num = all_df.shape[0]
    offset_train = int(num * traning_ratio)
    offset_val = int(num * validation_ratio)

    if num == 0 or offset_train < 1:
        return [], all_df
    if shuffle:
        all_df.sample(frac=1).reset_index(drop=True)
    train = all_df.loc[:offset_train]
    validation = all_df.loc[offset_train:offset_val]
    test = all_df.loc[offset_val:]
    train.to_csv('train.csv',index = False, sep=',')
    validation.to_csv('validation.csv',index=False, sep=',')
    test.to_csv('test.csv',index=False, sep=',')
    return train, validation, test


def read_labelled_data(labeled_data_path):
    print('>>> Reading labeled data...\n')
    labeled_data = pd.read_csv(labeled_data_path, low_memory=False)
    return labeled_data



def parse_labeled_data(labeled_data):

    labeled_data['left_title'] = ''
    labeled_data['right_title'] = ''
    labeled_data['left_model'] = ''
    labeled_data['right_model'] = ''
    for index, row in labeled_data.iterrows():
        [left_page_title, left_model] = get_info(row['left_spec_id'])
        [right_page_title, right_model] = get_info(row['right_spec_id'])
        labeled_data.at[index, 'left_title'] = left_page_title
        labeled_data.at[index, 'right_title'] = right_page_title
        labeled_data.at[index, 'left_model'] = left_model
        labeled_data.at[index, 'right_model'] = right_model

    labeled_data = labeled_data[['left_title', 'left_model', 'right_title', 'right_model', 'label']]
    return labeled_data


def get_info(spec_id):

    [website, id] = spec_id.split('//')
    id += '.json'
    data_path = os.path.join(dataset_path, website, id)
    with open(data_path) as f:
        file = json.load(f)
        page_title = file.get('<page title>')
        if 'model' in file:
            model = file.get('model')
        else:
            model = 'None'
    return [page_title, model]




submission_file_path = './data/modified_small_dataset.csv'
dataset_path = './data/2013_camera_specs'

data = read_labelled_data(submission_file_path)
parsed_data = parse_labeled_data(data)
split(parsed_data, shuffle=True, traning_ratio=0.6, validation_ratio=0.2, test_ratio=0.2)

train, validation, test = dm.data.process(
    path='',
    train='train.csv',
    validation='validation.csv',
    test='test.csv')

model = dm.MatchingModel(attr_summarizer='hybrid')
model.run_train(
    train,
    validation,
    epochs=10,
    batch_size=16,
    best_save_path='hybrid_model.pth',
    pos_neg_ratio=3)
model.run_eval(test)
