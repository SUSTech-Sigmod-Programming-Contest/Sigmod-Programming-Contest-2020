import pandas as pd
import os
import csv

dataset_path = './page_title'
output_path = './brandname'
brandList = ['Nikon', 'Kodak', 'Sony', 'Canon', 'Go Pro', 'GoPro', 'Olympus', 'Fuji', 'Samsung', 'Panasonic', 'Leica',
             'Vivitar', 'Pentax', 'Hikvision', 'Polaroid', 'Minolta', 'Casio', 'Ricoh', 'BenQ', 'Dahua', 'Cannon',
             'Toshiba', 'Minox', 'SVP', 'VistaQuest', 'Vista Quest', 'Vizio', 'JVC', 'Lexar', 'B+W',
             'BELL+HOWELL', 'Bell Howell ', 'Coleman', 'DJI', 'Hoya', 'SanDisk', 'Sekonic', 'Lytro Light Field',
             'Sanyo', 'Aquapix', 'Sigma SD', 'Aiptek',
             'Philips', 'HASSELBLAD', 'CELESTRON', 'Sigma DP', 'Pioneer Elite', 'Konica', 'Cobra', 'Sealife', 'Argus',
             'Skyworth', 'Seiki', 'Lowrance Elite','Kyocera','Staples Corrugated Shipping Boxes','coolpix']

# merge-pair: Knoica - Minolta ; coolpix-nikon
shortname_brandList = ['GE', 'LG', 'HP']
accessories_brandList = ['Lowepro', 'Samyang']
spelling_error = ['Fujufilm']
columns_df = ['id', 'page_title']
vis = {}


def blocking_in_general():
    for brand in brandList:
        data = {'id': [], 'page_title': []}
        for website in os.listdir(dataset_path):
            with open(dataset_path + '/' + website, 'r', encoding='UTF-8') as file:
                reader = csv.reader(file)
                i = False
                for row in reader:
                    if i:
                        num = row[0]
                        key = website[0:-4] + '//' + num
                        page_title = row[1]
                        if key not in vis:
                            vis[key] = 0
                        if page_title.lower().find(brand.lower()) != -1:
                            data['id'].append(key)
                            data['page_title'].append(page_title)
                            vis[key] += 1
                    else:
                        i = True
        df = pd.DataFrame(data, columns=columns_df)
        df.to_csv(output_path + '/' + brand + '.csv', index=False)
        print(brand)


def blocking_in_shortname():
    for brand in shortname_brandList:
        data = {'id': [], 'page_title': []}
        for website in os.listdir(dataset_path):
            with open(dataset_path + '/' + website, 'r', encoding='UTF-8') as file:
                reader = csv.reader(file)
                i = False
                for row in reader:
                    if i:
                        num = row[0]
                        key = website[0:-4] + '//' + num
                        page_title = row[1]
                        words = page_title.split(' ')
                        for word in words:
                            if word == brand:
                                data['id'].append(key)
                                data['page_title'].append(page_title)
                                vis[key] += 1
                    else:
                        i = True
        df = pd.DataFrame(data, columns=columns_df)
        df.to_csv(output_path + '/' + brand + '.csv', index=False)
        print(brand)


def collecting_remain():
    data = {'id': [], 'page_title': []}
    for website in os.listdir(dataset_path):
        with open(dataset_path + '/' + website, 'r', encoding='UTF-8') as file:
            reader = csv.reader(file)
            i = False
            for row in reader:
                if i:
                    num = row[0]
                    page_title = row[1]
                    key = website[0:-4] + '//' + num
                    if vis[key] == 0:
                        data['id'].append(key)
                        data['page_title'].append(page_title)
                else:
                    i = True
    df = pd.DataFrame(data, columns=columns_df)
    df.to_csv(output_path + '/' + 'others' + '.csv', index=False)


def blocking():
    blocking_in_general()
    blocking_in_shortname()
    collecting_remain()


blocking()
