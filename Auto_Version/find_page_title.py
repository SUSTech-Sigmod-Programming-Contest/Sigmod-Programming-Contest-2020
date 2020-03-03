import csv

dataset_path = './page_title/page_title.csv'


def find_page_title(key):
    with open(dataset_path, 'r', encoding='UTF-8') as file:
        reader = csv.reader(file)
        isNotFirstLine = False
        for row in reader:
            if isNotFirstLine:
                if row[0] == key:
                    return row[1]
            if not isNotFirstLine:
                isNotFirstLine = True

