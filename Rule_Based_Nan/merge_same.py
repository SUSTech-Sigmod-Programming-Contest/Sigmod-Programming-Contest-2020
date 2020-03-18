import re
import os
from merge import merge
import csv
import dataloader

prefix_dict = {
    'Canon': ['IXUS', 'ELPH', 'IXY', 'Powershot'],
    'Casio': ['EX'],
    'Fujifilm': ['Finepix'],
    'GE': [],
    'Olympus': [r'SP', r'E', r'TG', r'SZ', r'Stylus', r'x', r'XZ', r'TG', r'SH'],
    'Panasonic': ['DMC'],
    'Samsung': ['EC'],
    'Sony': ['NEX', 'DSC', 'DMC', 'DSLR', 'SLT'],
    'Nikon': ['Nikon']
}

meaningful_postfix_dict = {
    'Fujifilm': r'(s|t|w)',
    'Sony': r'(r|s|(M3)|(II)|(III)|(IV))',
    'Nikon': r'(s|x|e|h)',
}


def refine_model(brand_name, model_raw):
    model_clean = model_raw
    prefix_reg_list = prefix_dict[brand_name]
    if brand_name in meaningful_postfix_dict.keys():
        meaningful_postfix_reg = meaningful_postfix_dict[brand_name]
    else:
        meaningful_postfix_reg = None
    for reg in prefix_reg_list:
        prefix_ext = re.compile(r'^' + reg + r'[- ]?(.*)', re.I)
        if prefix_ext.findall(model_clean):
            tmp = prefix_ext.findall(model_clean)[0]
            if not re.match('[0-9]+[a-zA-Z]*$', tmp):
                model_clean = tmp
            else:
                model_clean = reg + tmp  # 去掉空格和-
    if re.match('[a-zA-Z]+[ -][0-9]+$', model_clean, re.I):
        tmp = re.findall('([a-zA-Z]+)[ -]([0-9]+)$', model_clean)
        model_clean = tmp[0][0] + tmp[0][1]
    if re.match('[a-zA-Z]+[0-9]+[a-zA-Z]+', model_clean):
        if not (meaningful_postfix_reg and re.match(r'.*' + meaningful_postfix_reg + r'$', model_raw, re.I)):
            model_clean = re.findall('([a-zA-Z]+[0-9]+)[-a-zA-Z]+', model_clean)[0]
    return model_clean


def extract_same_model(brand):
    brand_dir = './model/' + brand
    model_files = os.listdir(brand_dir)
    same_models = set()
    for file_name in model_files:
        model, _ = file_name.split('.')
        model_file_path = brand_dir + '/' + model + '.csv'
        with open(model_file_path, encoding='UTF-8') as model_file:
            reader = csv.reader(model_file)
            is_first_row = True
            for row in reader:
                if is_first_row:
                    is_first_row = False
                elif row:
                    model_label_content = dataloader.load_model(row[0])
                    if re.match('.* / .*', model_label_content):
                        same_models.add(tuple(model_label_content.split(' / ')))
    return same_models


if __name__ == '__main__':
    # print(extract_same_model('Canon'))
    for brand in prefix_dict.keys():
        print('Merge Same Model:', brand)
        dataset_path = './model/' + brand
        model_dict = {}
        for model_csv in os.listdir(dataset_path):
            model, _ = model_csv.split('.')
            refined_model = refine_model(brand, model)
            # print(model, refined_model)
            if refined_model not in model_dict:
                model_dict[refined_model] = []
            model_dict[refined_model].append(model)

        for item in model_dict.items():
            same_list = item[1]
            if len(same_list) > 1:
                for i in range(1, len(same_list)):
                    print('Merge:', same_list[i], 'to', same_list[0])
                    merge(same_list[0], same_list[i], dataset_path, 1)

        if brand == 'Panasonic':
            same_pairs = extract_same_model(brand)
            for tup in same_pairs:
                left, right = tup
                left = refine_model(brand, left)
                right = refine_model(brand, right)
                if left in model_dict and right in model_dict:
                    left_list = model_dict[left]
                    right_list = model_dict[right]
                    print('Merge:', left_list[0], 'to', right_list[0])
                    merge(right_list[0], left_list[0], dataset_path, 0)
