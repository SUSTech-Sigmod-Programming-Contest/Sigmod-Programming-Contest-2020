import os
import json
import pandas as pd

"""
这个文件负责所有和存储数据有关的任务，并提供将中间数据写入文件的方法
"""


"""
所有的数据应该是一个映射，key为source，value为json文件
"""
all_data = {}

# """
# 提取出page_title作为列表
# """
# page_titles = []

# """
# 解析完page_title后会得到所有的品牌
# """
# brand_set = set()

"""
对每个商品分好品牌
key值为品牌名称，value为该品牌下所有型号的list
"""
brand_index = {}

# """
# 对每个品牌都解析完成后会得到品牌和该品牌下所有型号的映射
# key值为品牌的名称，value值为该品牌下所有型号的list
# """
# brand_models = {}

"""
二维映射
第一维：key值为品牌的名称，value值为该品牌下所有型号及其对应所有相机的映射
第二维：key值为型号名称，value值维该型号所有相机的list
"""
model_index = {}


"""
倒排索引
key值为specification id
value值为（品牌型号）
"""
reverse_index = {}



"""

"""
others = {}


def read_all(data_path):
    """
    把所有数据读入all_data的字典中
    """
    print("Reading all data into memory...")
    for website in os.listdir(data_path):
        print("Reading website: ", website)
        website_path = os.path.join(data_path, website)
        products = os.listdir(website_path)
        for product_file in products:
            spec_id = website + '//' + product_file[0:-5]
            f_path = os.path.join(website_path, product_file)
            with open(f_path, encoding='UTF-8') as f:
                json_content = json.load(f)
                all_data[spec_id] = json_content

    print(len(all_data))


def collect_remain():
    for brand, brand_items in model_index.items():
        all_set = set(brand_index[brand])
        exist_set = set()
        for model, model_items in brand_items.items():
            for item in model_items:
                exist_set.add(item)
        others[brand] = all_set - exist_set


def brand_index_to_file(output_path):
    print("Writing brand index to file...")
    column_df = ['id', '<page title>']
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    for brand_name, brand_items in brand_index.items():
        output_dict = {'id': [], '<page title>': []}
        brand_output_path = os.path.join(output_path, brand_name + '.csv')
        for item in brand_items:
            output_dict['id'].append(item)
            output_dict['<page title>'].append(all_data[item].get('<page title>'))
        df = pd.DataFrame(output_dict, columns=column_df)
        df.to_csv(brand_output_path, index=False)


def model_index_to_file(output_path, write_others=True):
    print("Writing model index to file...")
    column_df = ['id', '<page title>']
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    for brand_name, model_dict in model_index.items():
        brand_output_path = os.path.join(output_path, brand_name)
        if not os.path.exists(brand_output_path):
            os.makedirs(brand_output_path)
        for model_name, model_items in model_dict.items():
            output_dict = {'id': [], '<page title>': []}
            model_output_path = os.path.join(brand_output_path, model_name + '.csv')
            for item in model_items:
                output_dict['id'].append(item)
                output_dict['<page title>'].append(all_data[item].get('<page title>'))
            df = pd.DataFrame(output_dict, columns=column_df)
            df.to_csv(model_output_path, index=False)
        # write others.csv
        if write_others:
            output_dict = {'id': [], '<page title>': []}
            model_output_path = os.path.join(brand_output_path, 'others.csv')
            if brand_name in others:
                for item in others[brand_name]:
                    output_dict['id'].append(item)
                    output_dict['<page title>'].append(all_data[item].get('<page title>'))
                df = pd.DataFrame(output_dict, columns=column_df)
                df.to_csv(model_output_path, index=False)
            else:
                print("NO others in brand", brand_name)





if __name__ == '__main__':
    # read_all("./2013_camera_specs")
    pass

