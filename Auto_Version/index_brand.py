import pandas as pd
import os
import json
from edit_distance import *
from find_page_title import *

dataset_path = './2013_camera_specs'
special_brand = ['Hikvision', 'Dahua', 'Konica', 'Cannon', 'Coolpix', 'Vista Quest', 'Go Pro']
ban_list = {'Tamron': 1, 'SHOOT': 1}
columns_df = ['id', '<page title>']
brand_list = []
brand_items = {}
brand_exist = {}


def test_valid_brand(brand):
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
        if len(temp) > 1 and temp[0] in brand_exist:
            brand_list.remove(brand)
    return


def remove_low_frequency():
    brand_candidate = sorted(brand_exist.items(), key=lambda x: -x[1])
    brand_exist.clear()
    for brand in brand_candidate:
        if brand[1] > len(brand_candidate) * 0.01:
            brand_list.append(brand[0])
            brand_exist[brand[0]] = 1
        else:
            break
    return


def add_special():
    for brand in special_brand:
        brand_list.append(brand)
    return


def get_brand_list():
    for website in os.listdir(dataset_path):
        website_path = dataset_path + '/' + website
        fileList = os.listdir(website_path)
        for file in fileList:
            [id, forma] = file.split('.')
            key = website + '//'
            file = website_path + '/' + file
            key += id + ''
            f = open(file)
            attributes = json.load(f)
            for attribute in attributes:
                if attribute.lower() == 'brand':
                    brand = attributes.get(attribute)
                    if isinstance(brand, list):
                        brand = brand[0]
                    if not test_valid_brand(brand):
                        continue
                    if brand not in brand_exist:
                        brand_items[brand] = []
                        brand_items[brand].append(key)
                        brand_exist[brand] = 0
                    brand_exist[brand] += 1
                    brand_items[brand].append(key)
    remove_low_frequency()
    remove_duplicate()
    add_special()
    return brand_list


def make_dir():
    if not os.path.exists('brand'):
        os.makedirs('brand')
    for brand in brand_list:
        if not os.path.exists('./brand/' + brand):
            os.makedirs('./brand/' + brand)

    if not os.path.exists('model'):
        os.makedirs('model')
    for brand in brand_list:
        if not os.path.exists('./model/' + brand):
            os.makedirs('./model/' + brand)
    return


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


def isNotChineseBrand(brand):
    if brand == 'Hikvision' or brand == 'Dahua':
        return False
    return True


def blocking():
    for brand in brand_list:
        visit = {}
        Flag = isNotChineseBrand(brand)
        data = {'id': [], '<page title>': []}
        with open('./page_title/page_title.csv', 'r', encoding='UTF-8') as file:
            reader = csv.reader(file)
            isNotFirstLine = False
            for row in reader:
                if isNotFirstLine:
                    if match(brand, row[1]):
                        if Flag and row[0].find('www.alibaba.com') != -1:
                            continue
                        if row[0].find('www.ebay.com') != -1 and row[1].lower().find('lot of') != -1:
                            continue
                        visit[row[0]] = 1
                        add_data(data, row[0], row[1])
                else:
                    isNotFirstLine = True
        if brand in brand_items:
            for item in brand_items[brand]:
                if item not in visit:
                    visit[item] = 1
                    add_data(data, item, find_page_title(item))
        df = pd.DataFrame(data, columns=columns_df)
        df.to_csv('./brand/' + brand + '/' + brand + '.csv', index=False)


def merge(to_brand, from_brand):
    from_path = './brand/' + from_brand + '/' + from_brand + '.csv'
    to_path = './brand/' + to_brand + '/' + to_brand + '.csv'
    duplicate = {}
    data = {'id': [], '<page title>': []}
    with open(to_path, 'r', encoding='UTF-8') as file:
        reader = csv.reader(file)
        i = False
        for row in reader:
            if i:
                duplicate[row[0]] = 1
                data['id'].append(row[0])
                data['<page title>'].append(row[1])
            else:
                i = True
    with open(from_path, 'r', encoding='UTF-8') as file:
        reader = csv.reader(file)
        i = False
        for row in reader:
            if i:
                if row[0] not in duplicate:
                    data['id'].append(row[0])
                    data['<page title>'].append(row[1])
            else:
                i = True
    df = pd.DataFrame(data, columns=columns_df)
    df.to_csv(to_path, index=False)
    os.remove(from_path)
    os.removedirs('./brand/' + from_brand)


def merge_pair():
    for i in range(0, len(brand_list)):
        for j in range(i + 1, len(brand_list)):
            ed = calculate_Edit_Distance(brand_list[i], brand_list[j])
            if ed < 2 or brand_list[i].find(brand_list[j]) != -1 or brand_list[j].find(brand_list[i]) != -1:
                merge(brand_list[i], brand_list[j])
    merge('Nikon', 'Coolpix')


if __name__ == '__main__':
    print("Getting brand list...")
    get_brand_list()
    make_dir()
    print("Resolve by brand...")
    blocking()
    print("Merge brands...")
    merge_pair()
    print("Finish!")
    print()
