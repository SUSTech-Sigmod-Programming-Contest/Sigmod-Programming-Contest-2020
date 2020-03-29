from resolve_others_param import identify_model_param
from edit_distance import calculate_Edit_Distance
import re
import os
from merge import merge
from resolve_others_param import identify_model
import csv
import dataloader


def merge_similar():
    for brand in os.listdir('./model'):
        print(brand)
        brand_dir = './model/' + brand
        model_files = os.listdir(brand_dir)
        models = []
        for file_name in model_files:
            model, _ = file_name.split('.')
            models.append(model)

        dig_ext = re.compile('\d+')
        for i in range(len(models)):
            for j in range(i+1, len(models)):
                if calculate_Edit_Distance(models[i], models[j]) < 3:
                    if dig_ext.findall(models[i]) != dig_ext.findall(models[j]):
                        continue
                    if models[i][:2] != models[j][:2] or models[i][-1] == models[j][-1]:
                        continue
                    param_i = identify_model(brand, models[i])
                    param_j = identify_model(brand, models[j])
                    tup_i_1, tup_i_2 = param_i
                    if not tup_i_1 or not tup_i_2:
                        continue
                    if param_i != (None, None) and param_i == param_j:
                        print(models[i], models[j])
                        print(identify_model(brand, models[i]))
                        # merge(models[i], models[j], brand_dir, 0)


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
                else:
                    model_label_content = dataloader.load_model(row[0])
                    if re.match('.* / .*', model_label_content):
                        same_models.add(model_label_content)
    for same_pair in same_models:
        print(same_pair)


if __name__ == '__main__':
    extract_same_model('Panasonic')
    # merge_similar()






