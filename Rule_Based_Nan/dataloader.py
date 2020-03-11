import os
import json

DATASET_PATH = './2013_camera_specs'


def load_json(index):
    source, specification_num = index.split("//")
    specification = specification_num + ".json"
    with open(os.path.join(DATASET_PATH, source, specification)) as specification_file:
        return json.load(specification_file)


def load_page_title(index):
    return load_json(index).get('<page title>')


def load_model(index):
    model = load_json(index).get('model')
    if model:
        if isinstance(model, list):
            concat_model = model[0]
            for i in range(1, len(model)):
                concat_model = concat_model + ' ' + model[i]
            return concat_model
        else:
            return model
    else:
        return 'NO-MODEL'


