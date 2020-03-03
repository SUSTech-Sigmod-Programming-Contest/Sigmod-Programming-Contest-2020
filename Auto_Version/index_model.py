import os
import csv
import pandas as pd
import re

columns_df = ['id', '<page title>']
ban_list = {'1080p': 1, '720p': 1, '3d': 1}
prefix_ban_list = {'under': 1, 'with': 1, 'camera': 1, 'full': 1, 'black': 1, 'pink': 1, 'for': 1, 'body': 1,
                   'canon': 1, 'ef': 1, 'top': 1, 'w': 1, 'led': 1, 'tv': 1, 'kit': 1}
special_model = {'Canon': ['xt', 'xti', 'xs', 'xsi', 'eos-1d', 'eos m'],
                 'Nikon': ['df', 'v1', 'v2', 'd1x', 'd2x', 'd3x']}
dataset_path = './brand'
output_path = './model'
vis = {}

if not os.path.exists('./model'):
    os.makedirs('./model')


def collecting_models(page_title, model_exist, model_list):
    temp = page_title.split(" ")
    for i in range(0, len(temp) - 1):
        '''
            型号提取规则1：由一个单词组成
            1) 长度大于等于2且如果长度小于等于3，最后一位不为x
            2) 最后一位是字母，除了最后一位是数字
            3) 第一位为字母，且型号包含字母和数字且仅有字母和数字和“-”组成
        '''
        for step in range(2):
            word = temp[i+step]
            if len(word) < 2 or (len(word) <= 3 and word[len(word)-1].lower() == 'x') or \
                    word.lower() in ban_list:
                return
            if re.match('[0-9]+[a-zA-Z]$', word):
                if word.lower() in model_exist:
                    return
                model_exist[word.lower()] = 1
                model_list.append(word)
                return
            elif re.match('[a-zA-Z][0-9a-zA-Z-]+$', word) and \
                    re.search('[0-9]', word):
                if word.lower() in model_exist:
                    return
                model_exist[word.lower()] = 1
                model_list.append(word)


        '''
        if rule1(word) and word.lower() not in ban_list:
            if word.lower() in model_exist:
                return
            model_exist[word.lower()] = 1
            model_list.append(word)
            return
        '''
        '''
        word = temp[i + 1]
        if rule1(word) and word.lower() not in ban_list:
            if word.lower() in model_exist:
                return
            model_exist[word.lower()] = 1
            model_list.append(word)
            return
        '''

        # if all_English_alphabet(temp[i]) and temp[i].lower() not in prefix_ban_list and all_digital(temp[i + 1]):
        '''
            型号提取规则2：由两个单词组成
            第一个词由字母组成，第二个词由长度为3-5的数字或2-4位数字+1位部位x的字母组成。
        '''
        if re.match('[a-zA-Z]+$', temp[i]) and \
                temp[i].lower() not in prefix_ban_list and \
                re.match('[0-9]{1,4}[0-9a-wy-zA-WY-Z]$', temp[i+1]):
            word = temp[i] + ' ' + temp[i + 1]
            if word.lower() in model_exist:
                return
            model_exist[word.lower()] = 1
            model_list.append(word)
            return


'''
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
'''


'''
def rule1(word):
    score = 0
    if len(word) < 2:
        return False
    if len(word) <= 3 and word[len(word) - 1].lower() == 'x':
        return False
    Flag = True # Flag 代表除最后一位为数字
    for i in range(0, len(word) - 1):
        if not word[i].isdigit():
            Flag = False
            break
    if word[len(word) - 1].isalpha() and Flag:  # 最后一位是字母，除了最后一位是数字
        return True
    if not word[0].isalpha():
        return False
    for alphabet in word:    # 第一位为字母，且型号仅有字母和数字和“-”组成
        if alphabet.isalpha():
            score |= 1
        elif alphabet.isdigit():
            score |= 2
        elif alphabet != "-":
            score |= 4
    if score == 3:
        return True
    return False
'''


def find_models(file, model_exist, model_list):
    with open(file, 'r', encoding='UTF-8') as f:
        reader = csv.reader(f)
        is_not_first_line = False
        for row in reader:
            if is_not_first_line:
                page_title = row[1]
                collecting_models(page_title, model_exist, model_list)
            else:
                is_not_first_line = True


def matching(website, file, model_list):
    for model in model_list:
        data = {'id': [], '<page title>': []}
        with open(file, 'r', encoding='UTF-8') as f:
            reader = csv.reader(f)
            is_not_first_line = False
            for row in reader:
                if is_not_first_line:
                    key = row[0]
                    page_title = row[1]
                    temp = page_title.split(" ")
                    for word in temp:
                        if word.lower() == model.lower():
                            vis[key] = 1
                            data['id'].append(key)
                            data['<page title>'].append(page_title)
                        if re.match('[a-z]+[0-9]+[a-z]+$', word.lower()):
                            part = re.findall('([a-z]+[0-9]+)', word.lower())[0]
                            if part == model.lower():
                                vis[key] = 1
                                data['id'].append(key)
                                data['<page title>'].append(page_title)
                            else:
                                tmp_word = re.findall('[a-z]+', part)[0] + ' ' + re.findall('[0-9]+', part)[0]
                                if tmp_word == model.lower():
                                    vis[key] = 1
                                    data['id'].append(key)
                                    data['<page title>'].append(page_title)
                    for i in range(0, len(temp) - 1):
                        word = temp[i] + ' ' + temp[i + 1]
                        if word.lower() == model.lower():
                            vis[key] = 1
                            data['id'].append(key)
                            data['<page title>'].append(page_title)
                        word = temp[i] + temp[i + 1]
                        if word.lower() == model.lower():
                            vis[key] = 1
                            data['id'].append(key)
                            data['<page title>'].append(page_title)
                else:
                    is_not_first_line = True
        df = pd.DataFrame(data, columns=columns_df)
        df.to_csv(output_path + '/' + website + '/' + model + '.csv', index=False)


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
        if brand in special_model:
            for model in special_model[brand]:
                model_list.append(model)
                model_exist[model] = 1
        file = website_path + '/' + file
        print("Getting model list...")
        find_models(file, model_exist, model_list)
        print("Resolve by model...")
        matching(website, file, model_list)
        print("Merge models...")
        remove_path = merge_pair(model_list, brand)
        print("Remove non-contribute...")
        kill_non_contribute()
        print("Finish!")
        for path in remove_path:
            if os.path.exists(path):
                os.remove(path)
        print()
