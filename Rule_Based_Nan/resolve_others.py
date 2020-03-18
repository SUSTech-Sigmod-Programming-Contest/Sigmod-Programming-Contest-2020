import csv
import re
from merge_same import prefix_dict
import pandas as pd
import os


def resolve_others(brand):
    dataset_path = './model/' + brand
    prefix_reg_list = prefix_dict[brand]
    if 'others.csv' in os.listdir(dataset_path):
        others_path = dataset_path + '/others.csv'
    else:
        others_path = None
    file_others = open(others_path, encoding='UTF-8')
    reader = csv.reader(file_others)
    models = {}
    new_others_dict = {'id':[], '<page_title>':[]}
    columns_df = ['id', '<page_title>']
    is_first_line = True
    for row in reader:
        if is_first_line:
            is_first_line = False
        else:
            found_flag = False
            for prefix in prefix_reg_list:
                reg_ext = re.compile(r'[ ,]' + prefix + r'[ -]?[0-9]+[a-zA-Z]*[ ,]?', re.I)
                if reg_ext.findall(row[1]):
                    found_flag = True
                    model_name = reg_ext.findall(row[1])[0][1:-1]
                    if model_name not in models:
                        models[model_name] = {'id': [], '<page_title>': []}
                    models[model_name]['id'].append(row[0])
                    models[model_name]['<page_title>'].append(row[1])
            if not found_flag:
                new_others_dict['id'].append(row[0])
                new_others_dict['<page_title>'].append(row[1])
    for each_model in models.items():
        output_dict = each_model[1]
        # print(each_model[0], len(each_model[1]['id']), each_model[1])
        output_path = dataset_path + '/' + each_model[0] + '.csv'
        if output_path in os.listdir(dataset_path):
            print('merge file: ', output_path, 'already exists')
            with open(output_path, encoding='UTF-8') as f:
                reader_2 = csv.reader(f)
                is_first_line_2 = True
                for row in reader_2:
                    if is_first_line_2:
                        is_first_line_2 = False
                    else:
                        output_dict['id'].append(row[0])
                        output_dict['<page_title>'].append(row[1])
        print("new model resolved:", each_model[0])
        output_df = pd.DataFrame(output_dict, columns=columns_df)
        output_df.to_csv(output_path, index=False)
    file_others.close()
    new_others_df = pd.DataFrame(new_others_dict, columns=columns_df)
    new_others_df.to_csv(others_path, index=False)
    # print('length of others:', len(new_others_dict['id']))


if __name__ == '__main__':
    for brand in prefix_dict.keys():
        print('resolve others:', brand)
        resolve_others(brand)
