import os
import csv
import pandas as pd

columns_df = ['left_spec_id', 'right_spec_id']


def merge(to_model, from_model, dataset_path):
    from_path = dataset_path + '/' + from_model + '.csv'
    to_path = dataset_path + '/' + to_model + '.csv'
    data = {'left_spec_id': [], 'right_spec_id': []}
    with open(to_path, 'r', encoding='UTF-8') as file:
        reader = csv.reader(file)
        i = False
        for row in reader:
            if i:
                data['left_spec_id'].append(row[0])
                data['right_spec_id'].append(row[1])
            else:
                i = True
    with open(from_path, 'r', encoding='UTF-8') as file:
        reader = csv.reader(file)
        i = False
        for row in reader:
            if i:
                data['left_spec_id'].append(row[0])
                data['right_spec_id'].append(row[1])
            else:
                i = True
    df = pd.DataFrame(data, columns=columns_df)
    df.to_csv(to_path, index=False)
    os.remove(from_path)


merge('submission', 'duplicate', './judge')
