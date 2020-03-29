import re
import csv
import dataloader


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
    reg_ext_1 = re.compile(r'([0-9]{1,2}\.[0-9]?)[ -]{0,1}MP', re.I)
    reg_ext_2 = re.compile(r' ([0-9]{1,2}?)[ -]([0-9]?)[ ]{0,1}MP', re.I)
    reg_ext_3 = re.compile(r'([0-9]{1,2}?)[ ]{0,1}MP', re.I)
    reg_ext_4 = re.compile(r'([0-9]{1,2}\.[0-9]?)[ -]{0,1}Mega[ ]{0,1}pixel', re.I)
    reg_ext_5 = re.compile(r' ([0-9]{1,2}?)[ -]([0-9]?)[ ]{0,1}Mega[ ]{0,1}pixel', re.I)
    reg_ext_6 = re.compile(r'([0-9]{1,2}?)[ ]{0,1}Mega[ ]{0,1}pixel', re.I)

    mp_1 = reg_ext_1.findall(page_title)
    mp_2 = reg_ext_2.findall(page_title)
    mp_3 = reg_ext_3.findall(page_title)
    mp_4 = reg_ext_4.findall(page_title)
    mp_5 = reg_ext_5.findall(page_title)
    mp_6 = reg_ext_6.findall(page_title)

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
        float_reg_ext = re.compile(r'\d+\.?\d*')
        result_mp = None
        for label in json_content:
            if re.search('pixel', label):
                useful_label = json_content.get(label)
                if isinstance(useful_label, list):
                    useful_label = useful_label[0]
                if float_reg_ext.findall(useful_label):
                    mp_tmp = float(float_reg_ext.findall(useful_label)[0])
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
            '''
                screen size的表现形式：
                1）num"
                2）num in
                3）纯数字
            '''
            label_content = json_content.get(label)
            if isinstance(label_content, list):
                label_content = label_content[0]

            reg_ext_1 = re.compile('(\d+\.?\d*)\"', re.I)
            reg_ext_2 = re.compile('(\d+\.?\d*) in', re.I)

            size_1 = reg_ext_1.findall(label_content)
            size_2 = reg_ext_2.findall(label_content)

            if size_1 and float(size_1[0]) < 50:
                screen_size = size_1[0]
            elif size_2 and float(size_2[0]) < 50:
                screen_size = size_2[0]
        elif re.search('(screen|display) size', label):
            label_content = json_content.get(label)
            if isinstance(label_content, list):
                label_content = label_content[0]
            reg_ext_3 = re.compile('(\d+\.?\d*)', re.I)
            size_3 = reg_ext_3.findall(label_content)
            if size_3 and float(size_3[0]) < 50:
                screen_size = size_3[0]

    if screen_size:
        return float(screen_size)
    else:
        return None


def extract_optical_zoom(json_content):
    for label in json_content:
        if re.search('optical zoom', label):
            return json_content.get(label)
    return None


def extract_mpn(json_content):
    return json_content.get('mpn')


def extract_model_params(brand, model, *extractors):
    """
        通过某一型号的数据来返回这一型号所对应的像素以及屏幕大小
        以投票决策的方式确定
        :param: 某一品牌具体型号的路径
        :return: 此型号产品对应的像素以及屏幕大小
        """
    model_path = './model/' + brand + '/' + model + '.csv'
    ext_dicts = []
    ext_ret = []
    with open(model_path, encoding='UTF-8') as model_file:
        is_first_row = True
        reader = csv.reader(model_file)
        for row in reader:
            if is_first_row:
                is_first_row = False
                for i in range(len(extractors)):
                    ext_dicts.append({})
            else:
                json_content = dataloader.load_json(row[0])
                for i in range(len(extractors)):
                    ext_dict = ext_dicts[i]
                    extractor = extractors[i]
                    ext_result = extractor(json_content)
                    if ext_result is not None:
                        if ext_result not in ext_dict:
                            ext_dict[ext_result] = 0
                        ext_dict[ext_result] += 1
        for i in range(len(extractors)):
            ext_dict = ext_dicts[i]
            ext_result_sorted = sorted(ext_dict.items(), key=lambda item: item[1], reverse=True)
            if ext_result_sorted:
                ext_ret.append(ext_result_sorted[0][0])
            else:
                ext_ret.append(None)
    return tuple(ext_ret)


if __name__ == '__main__':
    '''
        
    '''