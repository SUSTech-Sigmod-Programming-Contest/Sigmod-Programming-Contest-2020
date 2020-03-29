import os
import csv
import pandas as pd
import preprocessing
from copy import *
import dataset

# page_title_list = copy(preprocessing.page_title)
dataset_path = './brand'
output_path = './model'

columns_df = ['id', '<page title>']
ban_list = {'1080p': 1, '720p': 1, '3d': 1, '8F': 1}
prefix_ban_list = {'under': 1, 'with': 1, 'camera': 1, 'full': 1, 'black': 1, 'pink': 1, 'for': 1, 'body': 1,
                   'canon': 1, 'ef': 1, 'top': 1, 'w': 1, 'led': 1, 'tv': 1, 'kit': 1, 'lens': 1, 'edition': 1,
                   'only': 1, 'pro': 1, 'ii': 1, 'iii': 1}
special_model = {'Canon': ['xt', 'xti', 'xs', 'xsi', 'eos m', 'eos m2', '1ds'],
                 'Nikon': ['df', 'v1', 'v2', 'd1x', 'd2x', 'd3x', 'coolpix A'],
                 'GoPro': ['Hero 3', 'Hero 2', 'Hero3+'],
                 'Hasselblad': ['Hasselblad']}

vis = {}


# if not os.path.exists('./model'):
#     os.makedirs('./model')


def collecting_models(page_title, model_exist, model_list):
    temp = page_title.split(" ")

    for i in range(0, len(temp) - 1):
        word = temp[i]
        if rule1(word) and word.lower() not in ban_list:
            if word.lower() in model_exist:
                return
            model_exist[word.lower()] = 1
            model_list.append(word.upper())
            return

        word = temp[i + 1]
        if rule1(word) and word.lower() not in ban_list:
            if word.lower() in model_exist:
                return
            model_exist[word.lower()] = 1
            model_list.append(word.upper())
            return

        if valid_prefix_test(temp[i]) and temp[i].lower() not in prefix_ban_list and valid_postfix_test(temp[i + 1]):
            word = temp[i] + ' ' + temp[i + 1]
            if word.lower() in model_exist:
                return
            model_exist[word.lower()] = 1
            model_list.append(word.upper())
            return


def valid_prefix_test(word):
    if len(word) < 1:
        return False
    for alphabet in word:
        if not alphabet.isalpha():
            return False
    return True


def valid_postfix_test(word):
    if len(word) < 2 or len(word) > 7:
        return False
    for i in range(0, len(word) - 1):
        if not word[i].isdigit():
            return False
    if not word[len(word) - 1].isalpha() and not word[len(word) - 1].isdigit():
        return False
    if word[len(word) - 1].lower() == 'x':
        return False
    return True


def rule1(word):
    score = 0
    if len(word) < 2:
        return False
    if len(word) <= 3 and word[len(word) - 1].lower() == 'x':
        return False
    Flag = True
    for i in range(0, len(word) - 1):
        if not word[i].isdigit():
            Flag = False
            break
    if word[len(word) - 1].isalpha() and Flag:
        return True
    if not word[0].isalpha():
        return False
    for alphabet in word:
        if alphabet.isalpha():
            score |= 1
        elif alphabet.isdigit():
            score |= 2
        elif alphabet != "-":
            score |= 4
    if score == 3:
        return True

    return False


# def find_models(file, model_exist, model_list):
#     with open(file, 'r', encoding='UTF-8') as f:
#         reader = csv.reader(f)
#         isNotFirstLine = False
#         for row in reader:
#             if isNotFirstLine:
#                 page_title = row[1]
#                 collecting_models(page_title, model_exist, model_list)
#             else:
#                 isNotFirstLine = True


def matching(brand, model_list):
    products = dataset.brand_index[brand]
    for model in model_list:
        dataset.model_index[brand][model] = []
        for product in products:
            page_title = dataset.all_data[product].get('<page title>')
            temp = page_title.split(' ')
            for word in temp:
                if word.lower() == model.lower():
                    vis[product] = 1
                    dataset.model_index[brand][model].append(product)
            for i in range(0, len(temp) - 1):
                word = temp[i] + ' ' + temp[i + 1]
                if word.lower() == model.lower():
                    vis[product] = 1
                    dataset.model_index[brand][model].append(product)


# def matching(website, file, model_list):
#     for model in model_list:
#         data = {'id': [], '<page title>': []}
#         with open(file, 'r', encoding='UTF-8') as f:
#             reader = csv.reader(f)
#             isNotFirstLine = False
#             for row in reader:
#                 if isNotFirstLine:
#                     key = row[0]
#                     page_title = row[1]
#                     temp = page_title.split(" ")
#                     for word in temp:
#                         if word.lower() == model.lower():
#                             vis[key] = 1
#                             data['id'].append(key)
#                             data['<page title>'].append(page_title)
#                     for i in range(0, len(temp) - 1):
#                         word = temp[i] + ' ' + temp[i + 1]
#                         if word.lower() == model.lower():
#                             vis[key] = 1
#                             data['id'].append(key)
#                             data['<page title>'].append(page_title)
#                 else:
#                     isNotFirstLine = True
#         df = pd.DataFrame(data, columns=columns_df)
#         df.to_csv(output_path + '/' + website + '/' + model + '.csv', index=False)


def kill_non_contribute():
    delete_list = []
    for brand, brand_items in dataset.model_index.items():
        for model, model_items in brand_items.items():
            if len(model_items) < 2:
                delete_list.append((brand, model))
    for delete_brand, delete_model in delete_list:
        del dataset.model_index[delete_brand][delete_model]

    # for brand in os.listdir('./model'):
    #     brand_path = output_path + '/' + brand
    #     fileList = os.listdir(brand_path)
    #     for file in fileList:
    #         file = brand_path + '/' + file
    #         cnt = 0
    #         with open(file, 'r', encoding='UTF-8') as f:
    #             reader = csv.reader(f)
    #             for row in reader:
    #                 cnt += 1
    #         if cnt < 3:
    #             os.remove(file)


def merge(to_model, from_model, brand):
    dataset.model_index[brand][to_model] += dataset.model_index[brand][from_model]
    dataset.model_index[brand][to_model] = list(set(dataset.model_index[brand][to_model]))


# def merge(to_model, from_model, brand):
#     from_path = './model/' + brand + '/' + from_model + '.csv'
#     to_path = './model/' + brand + '/' + to_model + '.csv'
#     duplicate = {}
#     data = {'id': [], '<page title>': []}
#     with open(to_path, 'r', encoding='UTF-8') as file:
#         reader = csv.reader(file)
#         i = False
#         for row in reader:
#             if i:
#                 duplicate[row[0]] = 1
#                 data['id'].append(row[0])
#                 data['<page title>'].append(row[1])
#             else:
#                 i = True
#     with open(from_path, 'r', encoding='UTF-8') as file:
#         reader = csv.reader(file)
#         i = False
#         for row in reader:
#             if i:
#                 if row[0] not in duplicate:
#                     data['id'].append(row[0])
#                     data['<page title>'].append(row[1])
#             else:
#                 i = True
#     df = pd.DataFrame(data, columns=columns_df)
#     df.to_csv(to_path, index=False)


def remove_space(model_str):
    model_str = model_str.lower()
    res = ''
    for i in range(0, len(model_str)):
        if model_str[i] == ' ' or model_str[i] == '-':
            continue
        res += model_str[i]
    return res


# def merge_pair(model_list, brand):
#     remove_path = []
#     for i in range(0, len(model_list)):
#         for j in range(i + 1, len(model_list)):
#             if remove_space(model_list[i]) == remove_space(model_list[j]):
#                 merge(model_list[i], model_list[j], brand)
#                 remove_path.append('./model/' + brand + '/' + model_list[j] + '.csv')
#     return remove_path


def merge_pairs(model_list, brand):
    remove_models = []
    for i in range(0, len(model_list)):
        for j in range(i + 1, len(model_list)):
            if remove_space(model_list[i]) == remove_space(model_list[j]):
                merge(model_list[i], model_list[j], brand)
                remove_models.append(model_list[j])
            # remove_path.append('./model/' + brand + '/' + model_list[j] + '.csv')
    for rm_model in set(remove_models):
        del dataset.model_index[brand][rm_model]


def index_model():
    print("Indexing models")
    for brand, product_list in dataset.brand_index.items():
        print("Indexing models: ", brand)
        dataset.model_index[brand] = {}
        model_list = []
        model_exist = {}

        # add special
        if brand in special_model:
            for model in special_model[brand]:
                model_list.append(model.upper())
                model_exist[model.lower()] = 1

        # find_models
        for product in product_list:
            page_title = dataset.all_data[product].get('<page title>')
            collecting_models(page_title, model_exist, model_list)

        # matching
        matching(brand, model_list)

        merge_pairs(model_list, brand)
        kill_non_contribute()


    # for brand in os.listdir(dataset_path):
    #     print(brand)
    #     brand_path = dataset_path + '/' + brand
    #     fileList = os.listdir(brand_path)
    #     for file in fileList:
    #         [brand, forma] = file.split('.')
    #         if not os.path.exists('./model/' + brand):
    #             os.makedirs('./model/' + brand)
    #         model_list = []
    #         model_exist = {}
    #         if brand in special_model:
    #             for model in special_model[brand]:
    #                 model_list.append(model)
    #                 model_exist[model] = 1
    #
    #         file = brand_path + '/' + file
    #         find_models(file, model_exist, model_list)
    #
    #         matching(brand, file, model_list)
    #
    #         for path in merge_pair(model_list, brand):
    #             if os.path.exists(path):
    #                 os.remove(path)
    #
    #         kill_non_contribute()


if __name__ == '__main__':
    index_model()
