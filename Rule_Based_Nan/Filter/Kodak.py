import os
import csv
import pandas as pd

dataset_path = './model/Kodak'
fileList = os.listdir(dataset_path)
columns_df = ['id', '<page title>']

print("Cleaning... Kodak")
for file in fileList:
    file_path = dataset_path + '/' + file
    data = {'id': [], '<page title>': []}
    with open(file_path, 'r', encoding='UTF-8') as f:
        reader = csv.reader(f)
        isNotFirstLine = False
        for row in reader:
            if isNotFirstLine:
                page_title = row[1]
                if page_title.find('Printer Dock') != -1 or page_title.find('2 Digital Cameras with') != -1:
                    continue
                data['id'].append(row[0])
                data['<page title>'].append(row[1])
            else:
                isNotFirstLine = True
    df = pd.DataFrame(data, columns=columns_df)
    df.to_csv(file_path, index=False)