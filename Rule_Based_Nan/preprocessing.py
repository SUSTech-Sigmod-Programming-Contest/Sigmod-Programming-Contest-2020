import os
import json

page_title = {}


def get_page_title(dataset_path):
    for website in os.listdir(dataset_path):
        website_path = dataset_path + '/' + website
        fileList = os.listdir(website_path)
        for file in fileList:
            key = website + '//' + file[0:-5]
            file = website_path + '/' + file
            f = open(file)
            attributes = json.load(f)
            for attribute in attributes:
                if attribute == '<page title>':
                    page_title[key] = attributes.get(attribute)
                    break


get_page_title('./2013_camera_specs')
