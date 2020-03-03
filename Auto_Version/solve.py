from tqdm import tqdm
import os
import csv
import pandas as pd

DATA_PATH = "./model"
columns_df = ['left_spec_id', 'right_spec_id']
data = {'left_spec_id': [], 'right_spec_id': []}


def solve():
    for source in tqdm(os.listdir(DATA_PATH)):
        for model in os.listdir(os.path.join(DATA_PATH, source)):
            if model == 'others.csv':
                #os.remove(DATA_PATH+'/'+source+'/'+model)
                continue
            with open(DATA_PATH + '/' + source + '/' + model, 'r', encoding='UTF-8') as file:
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

    df = pd.DataFrame(data, columns=columns_df)
    df.to_csv('./judge/submission.csv', index=False)


solve()
