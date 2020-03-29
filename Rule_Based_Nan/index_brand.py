import pandas as pd
from edit_distance import *
import preprocessing
import csv
from copy import *
import os
import json
import dataset

# dataset_path = './2013_camera_specs'
# page_title_list = copy(preprocessing.page_title)
columns_df = ['id', '<page title>']
brand_list = []
brand_items = {}
# brand_exist = {}

special_brand = ['Hikvision', 'Dahua', 'Konica', 'Cannon', 'Coolpix', 'Vista Quest', 'Go Pro']
ban_list = {'Tamron', 'SHOOT'}


def valid_brand_test(brand):
    if brand == 'unknown':
        return False
    temp = brand.split(" ")
    if len(temp) > 2:
        return False
    for word in temp:
        for alphabet in word:
            if not alphabet.isalpha():
                return False
    return True


def remove_duplicate():
    for brand in brand_list:
        temp = brand.split(" ")
        if len(temp) > 1 and temp[0] in brand_items:
            brand_list.remove(brand)


def remove_low_frequency():
    threshold = len(brand_items)
    del_list = []
    for brand, item_list in brand_items.items():
        if len(item_list) <= threshold * 0.01:
            del_list.append(brand)
        else:
            brand_list.append(brand)
    for del_item in del_list:
        del brand_items[del_item]

    # brand_candidate = sorted(brand_exist.items(), key=lambda x: -x[1])
    # brand_exist.clear()
    # for brand in brand_candidate:
    #     if brand[1] > len(brand_candidate) * 0.01:
    #         brand_list.append(brand[0])
    #         brand_exist[brand[0]] = 1
    #     else:
    #         break
    # return


def add_special():
    for brand in special_brand:
        brand_list.append(brand)


def get_brand_list():
    for product_id, product_json in dataset.all_data.items():
        brand = product_json.get('brand')
        if brand:
            if isinstance(brand, list):
                brand = brand[0]
            if not valid_brand_test(brand):
                continue
            if brand in ban_list:
                continue
            if brand not in brand_items:
                brand_items[brand] = []
            brand_items[brand].append(product_id)

    # for website in os.listdir(dataset_path):
    #     website_path = dataset_path + '/' + website
    #     fileList = os.listdir(website_path)
    #     for file in fileList:
    #         [id, forma] = file.split('.')
    #         key = website + '//'
    #         file = website_path + '/' + file
    #         key += id + ''
    #         f = open(file)
    #         attributes = json.load(f)
    #         for attribute in attributes:
    #             if attribute.lower() == 'brand':
    #                 brand = attributes.get(attribute)
    #                 if isinstance(brand, list):
    #                     brand = brand[0]
    #                 if not valid_brand_test(brand):
    #                     continue
    #                 if brand not in brand_exist:
    #                     brand_items[brand] = []
    #                     brand_items[brand].append(key)
    #                     brand_exist[brand] = 0
    #                 brand_exist[brand] += 1
    #                 brand_items[brand].append(key)
    remove_low_frequency()
    remove_duplicate()
    add_special()
    # return brand_list


# def make_dir():
#     if not os.path.exists('brand'):
#         os.makedirs('brand')
#     for brand in brand_list:
#         if not os.path.exists('./brand/' + brand):
#             os.makedirs('./brand/' + brand)
#
#     if not os.path.exists('model'):
#         os.makedirs('model')
#     for brand in brand_list:
#         if not os.path.exists('./model/' + brand):
#             os.makedirs('./model/' + brand)
#     return


def match(brand, page_title):
    if len(brand) < 4:
        temp = page_title.split(" ")
        for word in temp:
            if word == brand:
                return True
    elif page_title.lower().find(brand.lower()) != -1:
        return True
    return False


def add_data(data, key, page_title):
    data['id'].append(key)
    data['<page title>'].append(page_title)


def is_chinese_brand(brand):
    if brand == 'Hikvision' or brand == 'Dahua':
        return False
    return True


def blocking():
    for brand in brand_list:
        visit = set()
        flag = is_chinese_brand(brand)
        # data = {'id': [], '<page title>': []}
        ids = []
        for key, json_content in dataset.all_data.items():
            page_title = json_content.get('<page title>')
            if match(brand, page_title):
                if flag and key.find('www.alibaba.com') != -1:
                    continue
                if key.find('www.ebay.com') != -1 and page_title.lower().find('lot of') != -1:
                    continue
                visit.add(key)
                ids.append(key)
        if brand in brand_items:
            for brand_item in brand_items[brand]:
                if brand_item not in visit:
                    visit.add(brand_item)
                    ids.append(brand_item)
        dataset.brand_index[brand] = ids

        # for key in page_title_list:
        #     page_title = page_title_list[key]
        #     if match(brand, page_title):
        #         if flag and key.find('www.alibaba.com') != -1:
        #             continue
        #         if key.find('www.ebay.com') != -1 and page_title.lower().find('lot of') != -1:
        #             continue
        #         visit[key] = 1
        #         add_data(data, key, page_title)
        # if brand in brand_items:
        #     for item in brand_items[brand]:
        #         if item not in visit:
        #             visit[item] = 1
        #             add_data(data, item, page_title_list[item])
        # df = pd.DataFrame(data, columns=columns_df)
        # df.to_csv('./brand/' + brand + '/' + brand + '.csv', index=False)


def merge(to_brand, from_brand):
    if from_brand in dataset.brand_index and to_brand in dataset.brand_index:
        dataset.brand_index[to_brand] += dataset.brand_index[from_brand]
        del dataset.brand_index[from_brand]

    # from_path = './brand/' + from_brand + '/' + from_brand + '.csv'
    # to_path = './brand/' + to_brand + '/' + to_brand + '.csv'
    # duplicate = {}
    # data = {'id': [], '<page title>': []}
    # with open(to_path, 'r', encoding='UTF-8') as file:
    #     reader = csv.reader(file)
    #     i = False
    #     for row in reader:
    #         if i:
    #             duplicate[row[0]] = 1
    #             data['id'].append(row[0])
    #             data['<page title>'].append(row[1])
    #         else:
    #             i = True
    # with open(from_path, 'r', encoding='UTF-8') as file:
    #     reader = csv.reader(file)
    #     i = False
    #     for row in reader:
    #         if i:
    #             if row[0] not in duplicate:
    #                 data['id'].append(row[0])
    #                 data['<page title>'].append(row[1])
    #         else:
    #             i = True
    # df = pd.DataFrame(data, columns=columns_df)
    # df.to_csv(to_path, index=False)
    # os.remove(from_path)
    # os.removedirs('./brand/' + from_brand)


def merge_pair():
    for i in range(0, len(brand_list)):
        for j in range(i + 1, len(brand_list)):
            ed = calculate_Edit_Distance(brand_list[i], brand_list[j])
            if ed < 2 or brand_list[i].find(brand_list[j]) != -1 or brand_list[j].find(brand_list[i]) != -1:
                merge(brand_list[i], brand_list[j])
    merge('Nikon', 'Coolpix')


def index_brand():
    print("Indexing brand")
    print("Getting brand list...")
    get_brand_list()
    # make_dir()
    print("Blocking according to brand...")
    blocking()
    print("Merge same brands...")
    merge_pair()



if __name__ == '__main__':
    index_brand()
