import os
import csv
import dataloader
import re
import pandas as pd
from merge import merge


def extract_mp(json_content):
    """
        通过json文件的内容，获取相机的像素（单位：MP）
        :param 输入json文件的整个内容
        :return 输出一个浮点数，表示像素
    """
    page_title = json_content.get('<page title>')
    '''
        Megapixel在标题中的表现形式
        1) 小数（空格）MP
        2) 整数1 空格 整数2 （空格）MP
        3) 整数MP
        4)5)6) 1)2)3) 用Megapixels替代MP
    '''
    mp_regexp_1 = r'([0-9]{1,2}\.[0-9]?)[ -]{0,1}MP'
    mp_regexp_2 = r' ([0-9]{1,2}?)[ -]([0-9]?)[ ]{0,1}MP'
    mp_regexp_3 = r'([0-9]{1,2}?)[ ]{0,1}MP'
    mp_regexp_4 = r'([0-9]{1,2}\.[0-9]?)[ -]{0,1}Mega[ ]{0,1}pixel'
    mp_regexp_5 = r' ([0-9]{1,2}?)[ -]([0-9]?)[ ]{0,1}Mega[ ]{0,1}pixel'
    mp_regexp_6 = r'([0-9]{1,2}?)[ ]{0,1}Mega[ ]{0,1}pixel'
    mp_1 = re.findall(mp_regexp_1.lower(), page_title.lower())
    mp_2 = re.findall(mp_regexp_2.lower(), page_title.lower())
    mp_3 = re.findall(mp_regexp_3.lower(), page_title.lower())
    mp_4 = re.findall(mp_regexp_4.lower(), page_title.lower())
    mp_5 = re.findall(mp_regexp_5.lower(), page_title.lower())
    mp_6 = re.findall(mp_regexp_6.lower(), page_title.lower())

    megapixal = None
    if len(mp_1):
        megapixal = float(mp_1[0])
    elif len(mp_2):
        megapixal = float(mp_2[0][0] + '.' + mp_2[0][1])
    elif len(mp_3):
        megapixal = float(mp_3[0])
    if len(mp_4):
        megapixal = float(mp_4[0])
    elif len(mp_5):
        megapixal = float(mp_5[0][0] + '.' + mp_5[0][1])
    elif len(mp_6):
        megapixal = float(mp_6[0])

    '''
        如果不在标题中，找到可能出现MP的标签（包含pixel的标签） 从标签中抽取浮点数，
        若有多个标签候选，则选取最大的数作为MP值
    '''
    if not megapixal:
        mp_float_regexp = r'\d+\.?\d*'
        result_mp = None
        for label in json_content:
            if re.search('pixel', label):
                useful_label = json_content.get(label)
                if isinstance(useful_label, list):
                    useful_label = useful_label[0]
                if re.findall('\d+\.?\d*', useful_label):
                    mp_tmp = float(re.findall('\d+\.?\d*', useful_label)[0])
                    if not result_mp:
                        if mp_tmp < 50:
                            result_mp = mp_tmp
                    elif result_mp < mp_tmp < 50:
                        result_mp = mp_tmp
        megapixal = result_mp

    return megapixal


def extract_screen_size(json_content):
    """
        通过json文件的内容，获取相机的screen size（单位："）
        :param json_content 输入json文件的整个内容
        :return 一个浮点数，表示screen size
    """
    screen_size = None
    for label in json_content:
        if re.search('(screen|display)', label):
            label_content = json_content.get(label)
            '''
                screen size的表现形式：
                1）num"
                2）num in
                3）纯数字
            '''
            if isinstance(label_content, list):
                label_content = label_content[0]

            reg_ext_1 = re.compile('(\d+\.?\d*)\"', re.I)
            reg_ext_2 = re.compile('(\d+\.?\d*) in', re.I)
            reg_ext_3 = re.compile('(\d+\.?\d*)', re.I)

            size_1 = reg_ext_1.findall(label_content)
            size_2 = reg_ext_2.findall(label_content)
            size_3 = reg_ext_3.findall(label_content)

            if size_1:
                screen_size = size_1[0]
            elif size_2:
                screen_size = size_2[0]
            elif size_3:
                screen_size = size_3[0]

    if screen_size:
        return float(screen_size)
    else:
        return None


def identify_model_param(model_path):
    """
    通过某一型号的数据来返回这一型号所对应的像素以及屏幕大小
    以投票决策的方式确定
    :param: 某一品牌具体型号的路径
    :return: 此型号产品对应的像素以及屏幕大小
    """
    mp_dict = {}
    ss_dict = {}
    with open(model_path, encoding='UTF-8') as model_file:
        reader = csv.reader(model_file)
        is_first_row = True
        for row in reader:
            if is_first_row:
                is_first_row = False
            else:
                json_content = dataloader.load_json(row[0])
                mp = extract_mp(json_content)
                if mp is not None:
                    if mp not in mp_dict:
                        mp_dict[mp] = 0
                    mp_dict[mp] += 1
                screen_size = extract_screen_size(json_content)
                if screen_size is not None:
                    if screen_size not in ss_dict:
                        ss_dict[screen_size] = 0
                    ss_dict[screen_size] += 1

    # print(mp_dict)
    # print(ss_dict) // 字典里有一些能反映当前同一个型号的分区中有不同的像素，屏幕分布

    mp_sorted = sorted(mp_dict.items(), key=lambda item: item[1], reverse=True)
    ss_sorted = sorted(ss_dict.items(), key=lambda item: item[1], reverse=True)
    if mp_sorted:
        mp_ret = mp_sorted[0][0]
    else:
        mp_ret = None
    if ss_sorted:
        ss_ret = ss_sorted[0][0]
    else:
        ss_ret = None

    return mp_ret, ss_ret


def select_fit_model(model_dict, *param):
    """
    通过已得到的参数与型号的字典，找到与一组参数最匹配的相机
    TODO :一组参数可能推导出多个相机型号，使用规则找到最匹配的那一个
    :param model_dict: 预先得到的参数与型号的对应字典
    :param param: 参数（未来可能会边长）
    :return: 参数所对应的相机型号
    """
    # A naive implementation
    if param[0] in model_dict.keys():
        prob_list = model_dict[param[0]]
        if prob_list and len(prob_list) == 1:
            return prob_list[0]
        else:
            return None
    else:
        return None


if __name__ == '__main__':
    for brand in os.listdir('./model'):
        brand_path = './model/' + brand
        if 'others.csv' not in os.listdir(brand_path):
            continue
        print(brand)
        model_dict = {}
        for model_file_name in os.listdir(brand_path):

            model, _ = model_file_name.split('.')
            if model == 'others':
                continue
            model_path = brand_path + '/' + model_file_name
            if re.search('_tmp', model):  # DEBUG
                os.remove(model_path)
                continue
            mp, ss = identify_model_param(model_path)
            if mp or ss:
                if (mp, ss) not in model_dict.keys():
                    model_dict[(mp, ss)] = []
                model_dict[(mp, ss)].append(model)

        ''' 这个字典里是通过一组mp和ss找到的所有品牌
        for item in model_dict.items():
            print(item)
        '''

        resolve_dict = {}
        with open(brand_path + '/others.csv', encoding='UTF-8') as others_model:
            reader = csv.reader(others_model)
            is_first_row = True
            cnt = 0  # cnt记录此品牌的others可以通过mp和ss找到对应model列表的数量
            tot = 0  # tot记录此品牌的总数量（没啥用）
            for row in reader:
                if is_first_row:
                    is_first_row = False
                else:
                    json_data = dataloader.load_json(row[0])
                    mp = extract_mp(json_data)
                    ss = extract_screen_size(json_data)
                    model_fit = select_fit_model(model_dict, (mp, ss))
                    # model_fit 表示others中解析出的型号名
                    # print(model_fit)
                    # print(row[0], dataloader.load_page_title(row[0])) # debug用
                    if model_fit:  # 如果找到了合适的型号给参数匹配
                        if model_fit not in resolve_dict.keys():
                            resolve_dict[model_fit] = []
                        resolve_dict[model_fit].append(row[0])
                        cnt += 1
                    tot = tot + 1

            for item in resolve_dict.items():
                print(item[0])
                tmp_model = item[0] + '_tmp'
                tmp_path = brand_path + '/' + tmp_model + '.csv'
                data = {'id': [], '<page title>': []}
                resolve_list = item[1]
                for product_specification in resolve_list:
                    data['id'].append(product_specification)
                    data['<page title>'].append(dataloader.load_page_title(product_specification))
                columns_df = ['id', '<page title>']
                df = pd.DataFrame(data, columns=columns_df)
                df.to_csv(tmp_path, index=False)
                merge(item[0], tmp_model, brand_path, 0)



            ''' 
            # 此段输出注释可以查看解析效果
            for item in resolve_dict.items():
                print("#########################################")
                print(item[0])
                for source in item[1]:
                    print(dataloader.load_page_title(source))
                print(item[1])
            '''
            print('cnt:', cnt)
            print('tot:', tot)


