import os
import csv
import dataloader
import re
import pandas as pd
from merge import merge
from extractor import *


def identify_model(brand, model):
    path = './model/' + brand + '/' + model + '.csv'
    return identify_model_param(path)


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


def resolve_others():
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


if __name__ == '__main__':
    # for brand in os.listdir('./model'):
    #     print(brand)
    brand = 'Panasonic'
    brand_path = './model/' + brand
    # if 'others.csv' not in os.listdir(brand_path):
    #     continue
    with open(brand_path + '/DMC-fs3.csv', encoding='UTF-8') as others_model:
        reader = csv.reader(others_model)
        is_first_row = True
        cnt = 0
        tot = 0
        for row in reader:
            if is_first_row:
                is_first_row = False
            else:
                json_data = dataloader.load_json(row[0])
                ext_res = extract_optical_zoom(json_data)
                ext_res_2 = extract_mpn(json_data)
                if ext_res:
                    print(ext_res)
                    print(ext_res_2)
                    cnt += 1
                tot += 1

        print('cnt:', cnt)
        print('tot:', tot)
    # resolve_others()
