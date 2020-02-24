import os
import re
import json
import pandas as pd
from tqdm import tqdm


def create_df(dataset_path):
    """Function used to create a Pandas DataFrame containing specifications page titles

    Reads products specifications from the file system (DATASET_PATH) and creates a Pandas DataFrame where each row is a
    specification. The columns are 'source' (e.g. www.sourceA.com), 'spec_number' (e.g. 1) and the 'page title'.

    Returns:
        df (pd.DataFrame): The Pandas DataFrame containing specifications and page titles
    """

    print('Creating dataframe...\n')
    columns_df = ['source', 'spec_number', 'spec_id', 'specification_data']
    progressive_id = 0
    progressive_id2row_df = {}
    for source in tqdm(os.listdir(dataset_path)):
        for specification in os.listdir(os.path.join(dataset_path, source)):
            specification_number = specification.replace('.json', '')
            specification_id = '{}//{}'.format(source, specification_number)
            with open(os.path.join(dataset_path, source, specification)) as specification_file:
                specification_data = json.load(specification_file)
                row = (source, specification_number, specification_id, specification_data)
                progressive_id2row_df.update({progressive_id: row})
                progressive_id += 1
    df = pd.DataFrame.from_dict(progressive_id2row_df, orient='index', columns=columns_df)
    # print(df.head(5))
    print('Dataframe created successfully!')
    return df
