import re
import csv
import os
import pandas as pd
import dataset


def postfix_split(brand, model, postfixes):
    """
        考虑某型号的后缀将其分离。如1d和1dx
    """
    # path_parent = './model/' + brand
    # path = './model/' + brand + '/' + model + '.csv'
    # file = open(path, encoding='UTF-8')
    # reader = csv.reader(file)
    postfix_dict = {model: []}
    # is_first_line = True
    for postfix in postfixes:
        postfix_dict[model+postfix] = []
    # for row in reader:
    #     if is_first_line:
    #         is_first_line = False
    #         continue
    product_list = dataset.model_index[brand][model]
    for product in product_list:
        has_postfix = False
        for postfix in postfixes:
            reg_ext = re.compile(model[0] + r'[ ]?' + model[1] + r'[- ]?' + postfix, re.I)
            if reg_ext.search(dataset.all_data[product].get('<page title>')):
                postfix_dict[model+postfix].append(product)
                has_postfix = True
                break
        if not has_postfix:
            postfix_dict[model].append(product)
    # file.close()

    for new_model, model_list in postfix_dict.items():
        dataset.model_index[brand][new_model] = model_list
        # print(the_model)
        # if len(model_list) == 0:
        #     continue
        # already_exist = False
        # for f in os.listdir(path_parent):
        #     if re.match(the_model, f, re.I):
        #         the_model, _ = f.split('.')
        #         already_exist = True
        #         break
        # new_path = './model/' + brand + '/' + the_model + '.csv'
        # if already_exist and item[0] != model:
        #     with open(new_path, encoding='UTF-8') as new_file:
        #         reader = csv.reader(new_file)
        #         is_first_line = True
        #         for row in reader:
        #             if is_first_line:
        #                 is_first_line = False
        #                 continue
        #             model_list.append(row)
        # df = pd.DataFrame(model_list, columns=['id', '<page title>'])
        # df.to_csv(new_path, index=None)


def generation_split(brand, model, *spec_generations):
    """
        拆I, II, III, IV
    """
    # path_parent = './model/' + brand
    # path = './model/' + brand + '/' + model + '.csv'
    # file = open(path, encoding='UTF-8')
    # reader = csv.reader(file)
    product_list = dataset.model_index[brand][model]
    generation_dict = {model: []}
    generation_transfer = [(4, 'IV'),  (3, 'III'), (2, 'II')]
    for generation in generation_transfer:
        # print(generation[1]) # IV III II
        generation_dict[model + ' MARK ' + generation[1]] = []
    for spec_generation in spec_generations:
        generation_dict[model + ' ' + spec_generation] = []

    # is_first_line = True
    # for row in reader:
    #     if is_first_line:
    #         is_first_line = False
    #         continue
    for product in product_list:
        product_page_title = dataset.all_data[product].get('<page title>')
        is_spec = False
        for spec_generation in spec_generations:
            reg_ext = re.compile(spec_generation, re.I)
            if reg_ext.search(product_page_title):
                generation_dict[model + ' ' + spec_generation].append(product)
                is_spec = True
                break
        if is_spec:
            continue
        has_generation = False
        for generation in generation_transfer:
            # print(generation)
            reg_ext = re.compile('((MARK)|(MK))[ ]?(({})|({}))'
                                 .format(generation[0], generation[1]), re.I)
            if reg_ext.search(product_page_title):
                generation_dict[model + ' MARK ' + generation[1]].append(product)
                has_generation = True
                break
        if not has_generation:
            generation_dict[model].append(product)
    # file.close()

    for new_model, model_list in generation_dict.items():
        dataset.model_index[brand][new_model] = model_list
        # the_model = item[0]
        # model_list = item[1]
        # print(the_model)
        # if len(model_list) == 0:
        #     continue
        # new_path = './model/' + brand + '/' + the_model + '.csv'
        # df = pd.DataFrame(model_list, columns=['id', '<page title>'])
        # df.to_csv(new_path, index=None)


# def generation_split_check(brand, model):
#     path = './model/' + brand + '/' + model + '.csv'
#     file = open(path, encoding='UTF-8')
#     reader = csv.reader(file)
#     is_first_line = True
#     cnt = 0
#     for row in reader:
#         if is_first_line:
#             is_first_line = False
#             continue
#         if re.search(r'MARK I', row[1], re.I):
#             cnt += 1
#     file.close()
#     if cnt > 5:
#         return True
#     else:
#         return False


def split_brand():
    postfix_split('Canon', '1D', ['X', 'C', 'S'])
    postfix_split('Canon', 'G7', ['X'])
    generation_split('Canon', '1D', 'Mark II N')
    generation_split('Canon', '1DS')
    generation_split('Canon', '5D')
    generation_split('Canon', '7D')
    generation_split('Canon', 'G1')


# if __name__ == '__main__':
#     postfix_split('Canon', '1D', ['x', 'c', 's'])
#     postfix_split('Canon', 'G7', ['x'])
#     generation_split('Canon', '1D', 'Mark II n')
#     generation_split('Canon', '1DS')
#     generation_split('Canon', '5D')
#     generation_split('Canon', '7D')
#     generation_split('Canon', 'G1')

    # model_dir = './model'
    # for brand in os.listdir(model_dir):
    #     brand_path = model_dir + '/' + brand
    #     model_csv_files = os.listdir(brand_path)
    #     for model_csv_file in model_csv_files:
    #         model, _ = model_csv_file.split('.')
    #         if generation_split_check(brand, model):
    #             print(brand, model)

