from tqdm import tqdm
import os
import pandas as pd
import json
import numpy as np

DATASET_PATH = '../data/camera_specs'
LABELLED_DATA_PATH = '../data/sigmod_medium_labelled_dataset.csv'


class LabelledDataLoader:
    @staticmethod
    def load_json(index):
        source, specification_num = index.split("//")
        specification = specification_num + ".json"
        with open(os.path.join(DATASET_PATH, source, specification)) as specification_file:
            return json.load(specification_file)

    def __init__(self, dataset_dir_path, labelled_data_path):
        self.dataset_path = dataset_dir_path
        self.labelled_data_path = labelled_data_path
        dataset = []
        labels = []
        i = 0
        for line in open(LABELLED_DATA_PATH):
            if i == 0:
                i = 1
                continue
            index_left, index_right, label = line.split(",")
            left_page_title = self.load_json(index_left).get('<page title>')
            right_page_title = self.load_json(index_right).get('<page title>')
            dataset.append(np.array((left_page_title, right_page_title)))
            labels.append((np.array((label[0]))))  # label会附带\n
        self.dataset = np.array(dataset)
        self.labels = np.array(labels)

    def train_test_split(self, test_ratio=0.2, seed=None):
        assert 0.0 <= test_ratio <= 1.0, \
            "test_ratio must in (0, 1)"
        if seed:
            np.random.seed(seed)
        shuffle_indexes = np.random.permutation(len(self.dataset))
        test_size = int(len(self.dataset) * test_ratio)
        train_indexes = shuffle_indexes[test_size:]
        test_indexes = shuffle_indexes[:test_size]
        X_train = self.dataset[train_indexes]
        y_train = self.labels[train_indexes]
        X_test = self.dataset[test_indexes]
        y_test = self.labels[test_indexes]
        return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    dl = LabelledDataLoader(DATASET_PATH, LABELLED_DATA_PATH)
    X_train, X_test, y_train, y_test = dl.train_test_split()  # 可以获得训练集，测试集的numpy格式

    # 训练集和测试集每一行一一对应
    # 视情况选择numpy或DataFrame
    X_train_df = pd.DataFrame(X_train)
    X_train_df.columns = ["left-page-id", "right-page-id"]

    y_train_df = pd.DataFrame(y_train)
    y_train_df.columns = ["labels"]

    print(X_train_df)
    print(y_train_df)


