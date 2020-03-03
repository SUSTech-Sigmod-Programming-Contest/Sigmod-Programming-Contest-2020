from merge import *

dataset_path = './model/Panasonic'

fileList = os.listdir(dataset_path)
ban_list = {'f2': 1, 'f3': 1, 'lumix 14': 1}

print("Cleaning... Panasonic")
for file in fileList:
    file_path = dataset_path + '/' + file
    data = {'id': [], '<page title>': []}
    with open(file_path, 'r', encoding='UTF-8') as f:
        reader = csv.reader(f)
        isNotFirstLine = False
        for row in reader:
            if isNotFirstLine:
                page_title = row[1]
                if page_title.lower().find('flash kit for') != -1:
                    continue
                data['id'].append(row[0])
                data['<page title>'].append(row[1])
            else:
                isNotFirstLine = True
    df = pd.DataFrame(data, columns=columns_df)
    df.to_csv(file_path, index=False)

for file in fileList:
    [model, forma] = file.split('.')
    if model.lower() in ban_list:
        os.remove(dataset_path+'/'+file)

