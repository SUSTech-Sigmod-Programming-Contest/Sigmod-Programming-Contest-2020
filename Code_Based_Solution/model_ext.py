import os
from tqdm import tqdm
import json
# from cleaner.resources import brand_dic
from cleaner.data_loader import create_df
from nltk.corpus import wordnet
import re


DATASET_PATH = '../data/camera_specs'
OUTPUT_PATH = './output'


def is_terminology(word):
    term_list = [r'pictbrige', r'hdmi', r'^[0-9]+(\.[0-9]{1,2})?([xd]|(mp))?$', r'hd$', r'ptz$', r'cctv', r'usb'
                 r'for', r'with', '[0-9]*[g]']
    for term in term_list:
        if re.match(term.lower(), word.lower()):
            return True
    return False



def main():
    # columns_df = ['source', 'spec_number', 'spec_id', 'specification_data']
    df = create_df(DATASET_PATH)

    with open('./models.txt', 'w', encoding='UTF-8') as file:
        for index, row in tqdm(df.iterrows()):
            page_title = row["specification_data"].get("<page title>")
            new_str = ""
            words = []
            # print(re.split(r'( |,)', page_title))
            for word in re.split(r'[ ,\(\)]', page_title):
                if word == '-' or word == '':
                    continue
                if is_terminology(word):
                    continue
                if not wordnet.synsets(word):
                    new_str = new_str + word + ' '
                    words.append(word)
            print(words)


if __name__ == '__main__':
    main()
    # print(wordnet.synsets('Security'))









