import os
import csv
import pandas as pd
from edit_distance import *

columns_df = ['id', '<page title>']
ban_list = {'1080p': 1, '720p': 1}
prefix_ban_list = {'under': 1, 'with': 1, 'camera': 1, 'full': 1, 'black': 1, 'pink': 1, 'for': 1, 'body': 1,
                   'canon': 1, 'ef': 1, 'top': 1}
dataset_path = './brand'
output_path = './model'
vis = {}

if not os.path.exists('./model'):
    os.makedirs('./model')


def collecting_models(page_title, model_exist, model_list):
    temp = page_title.split(" ")
    for i in range(0, len(temp) - 1):
        word = temp[i]
        if rule1(word) and word.lower() not in ban_list:
            if word.lower() in model_exist:
                return
            model_exist[word.lower()] = 1
            model_list.append(word)
            return

        word = temp[i + 1]
        if rule1(word) and word not in ban_list:
            if word.lower() in model_exist:
                return
            model_exist[word.lower()] = 1
            model_list.append(word)
            return

        if all_English_alphabet(temp[i]) and temp[i].lower() not in prefix_ban_list and all_digital(temp[i + 1]):
            word = temp[i] + ' ' + temp[i + 1]
            if word.lower() in model_exist:
                return
            model_exist[word.lower()] = 1
            model_list.append(word)
            return


def all_English_alphabet(word):
    if len(word) < 1:
        return False
    for alphabet in word:
        if not alphabet.isalpha():
            return False
    return True


def all_digital(word):
    if len(word) < 2 or len(word) > 5:
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


def find_models(file, model_exist, model_list):
    with open(file, 'r', encoding='UTF-8') as f:
        reader = csv.reader(f)
        isNotFirstLine = False
        for row in reader:
            if isNotFirstLine:
                page_title = row[1]
                collecting_models(page_title, model_exist, model_list)
            else:
                isNotFirstLine = True


def matching(website, file, model_list):
    for model in model_list:
        data = {'id': [], '<page title>': []}
        with open(file, 'r', encoding='UTF-8') as f:
            reader = csv.reader(f)
            isNotFirstLine = False
            for row in reader:
                if isNotFirstLine:
                    key = row[0]
                    page_title = row[1]
                    temp = page_title.split(" ")
                    for word in temp:
                        if word.lower() == model.lower():
                            vis[key] = 1
                            data['id'].append(key)
                            data['<page title>'].append(page_title)
                    for i in range(0, len(temp) - 1):
                        word = temp[i] + ' ' + temp[i + 1]
                        if word.lower() == model.lower():
                            vis[key] = 1
                            data['id'].append(key)
                            data['<page title>'].append(page_title)
                else:
                    isNotFirstLine = True
        df = pd.DataFrame(data, columns=columns_df)
        df.to_csv(output_path + '/' + website + '/' + model + '.csv', index=False)


def collect_remain(website, file):
    data = {'id': [], '<page title>': []}
    with open(file, 'r', encoding='UTF-8') as f:
        reader = csv.reader(f)
        isNotFirstLine = False
        for row in reader:
            if isNotFirstLine:
                key = row[0]
                page_title = row[1]
                if key not in vis:
                    data['id'].append(key)
                    data['<page title>'].append(page_title)
            else:
                isNotFirstLine = True
    df = pd.DataFrame(data, columns=columns_df)
    df.to_csv(output_path + '/' + website + '/' + 'others.csv', index=False)


def kill_non_contribute():
    for website in os.listdir('./model'):
        website_path = output_path + '/' + website
        fileList = os.listdir(website_path)
        for file in fileList:
            file = website_path + '/' + file
            cnt = 0
            with open(file, 'r', encoding='UTF-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    cnt += 1
            if cnt < 3:
                os.remove(file)


def merge(to_model, from_model, brand):
    from_path = './model/' + brand + '/' + from_model + '.csv'
    to_path = './model/' + brand + '/' + to_model + '.csv'
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


def remove_space(str):
    str = str.lower()
    res = ''
    for i in range(0, len(str)):
        if str[i] == ' ' or str[i] == '-':
            continue
        res += str[i]
    return res


def merge_pair(model_list, brand):
    remove_path = []
    for i in range(0, len(model_list)):
        for j in range(i + 1, len(model_list)):
            if remove_space(model_list[i]) == remove_space(model_list[j]):
                merge(model_list[i], model_list[j], brand)
                remove_path.append('./model/' + brand + '/' + model_list[j] + '.csv')
    return remove_path


for website in os.listdir(dataset_path):
    print(website)
    website_path = dataset_path + '/' + website
    fileList = os.listdir(website_path)
    for file in fileList:
        [brand, forma] = file.split('.')
        if not os.path.exists('./model/' + brand):
            os.makedirs('./model/' + brand)
        model_list = []
        model_exist = {}
        file = website_path + '/' + file
        print("Getting model list...")
        find_models(file, model_exist, model_list)
        print("Resolve by model...")
        matching(website, file, model_list)
        print("Collect remain...")
        collect_remain(website, file)
        print("Merge models...")
        remove_path = merge_pair(model_list, brand)
        print("Remove non-contribute...")
        kill_non_contribute()
        print("Finish!")
        for path in remove_path:
            if os.path.exists(path):
                os.remove(path)
        print()
