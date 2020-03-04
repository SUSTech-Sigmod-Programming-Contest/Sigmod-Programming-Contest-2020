import pandas as pd
from tqdm import tqdm
import json
import csv
import os
import random
columns_df = ['left_spec_id', 'right_spec_id','label']

def find_positive(DATA_PATH):
    print('>>>finding positive matching')
    data = {'left_spec_id': [], 'right_spec_id': [], 'label': []}
    for model in os.listdir(DATA_PATH):
        if model == 'others.csv' or model == '.DS_Store':
            continue
        with open(DATA_PATH + '/' + model, 'r', encoding='UTF-8') as file:
            reader = csv.reader(file)
            temp = []
            k = False
            for row in reader:
                if k:
                    if len(row) > 1:
                        temp.append(row[0])
                else:
                    k = True
            for i in range(0, len(temp)):
                for j in range(i + 1, len(temp)):
                    data['left_spec_id'].append(temp[i])
                    data['right_spec_id'].append(temp[j])
                    data['label'].append('1')

    df = pd.DataFrame(data, columns=columns_df)
    df.to_csv('./data/dataset_generated.csv', index=False)

def find_negative(DATA_PATH, file1, file2):
    #print('>>>finding negative matching for '+file1+" and " + file2)
    with open(DATA_PATH + '/' + file1, 'r', encoding='UTF-8') as fileA:
        with open(DATA_PATH + '/' + file2, 'r', encoding='UTF-8') as fileB:
            data = {'left_spec_id': [], 'right_spec_id': [], 'label': []}
            readerA = csv.reader(fileA)
            readerB = csv.reader(fileB)

            tempA = []
            k1 = False
            for rowA in readerA:
                if k1:
                    if len(rowA) > 1:
                        tempA.append(rowA[0])
                else:
                    k1 = True

            tempB = []
            k2 = False
            for rowB in readerB:
                if k2:
                    if len(rowB) > 1:
                        tempB.append(rowB[0])
                else:
                    k2 = True
            count1 = 0
            count2 = 0

            random.shuffle(tempA)
            random.shuffle(tempB)
            for i in range(0, len(tempA)):
                for j in range(0, len(tempB)):
                    data['left_spec_id'].append(tempA[i])
                    data['right_spec_id'].append(tempB[j])
                    data['label'].append('0')
                    count1 = count1+1
                    if count1 > 0:
                        break
                count2 = count2 + 1
                if count2 > 1:
                    break
            df = pd.DataFrame(data, columns=columns_df)
            df.to_csv('./data/dataset_generated.csv', mode='a', header=False,index=False)


def combination(DATA_PATH):
    list = []
    combi = []
    for model in os.listdir(DATA_PATH):
        if model != 'others.csv' and model != '.DS_Store':
            list.append(model)
    for i in range(0,len(list)):
        for j in range(i+1, len(list)):
            combi.append([list[i],list[j]])
    return combi

if __name__ == '__main__':
    DATA_PATH = './data/Sony'
    find_positive(DATA_PATH)
    combi = combination(DATA_PATH)
    for pair in combi:
        find_negative(DATA_PATH,pair[0],pair[1])