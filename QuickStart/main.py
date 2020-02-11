import os
import json
import pandas as pd
import itertools
from tqdm import tqdm
import time

DATASET_PATH = './dataset'
OUTPUT_PATH = './output'


def create_dataframe():
    """Function used to create a Pandas DataFrame containing specifications page titles

    Reads products specifications from the file system (DATASET_PATH) and creates a Pandas DataFrame where each row is a
    specification. The columns are 'source' (e.g. www.sourceA.com), 'spec_number' (e.g. 1) and the 'page title'.

    Returns:
        df (pd.DataFrame): The Pandas DataFrame containing specifications and page titles
    """

    print('Creating dataframe...\n')
    columns_df = ['source', 'spec_number', 'spec_id', 'page_title']
    progressive_id = 0
    progressive_id2row_df = {}
    for source in tqdm(os.listdir(DATASET_PATH)):
        for specification in os.listdir(os.path.join(DATASET_PATH, source)):
            specification_number = specification.replace('.json', '')
            specification_id = '{}//{}'.format(source, specification_number)
            with open(os.path.join(DATASET_PATH, source, specification)) as specification_file:
                specification_data = json.load(specification_file)
                page_title = specification_data.get('<page title>').lower()
                row = (source, specification_number, specification_id, page_title)
                progressive_id2row_df.update({progressive_id: row})
                progressive_id += 1
    df = pd.DataFrame.from_dict(progressive_id2row_df, orient='index', columns=columns_df)
    print(df.head(5))
    print('Dataframe created successfully!')
    print()
    return df


def __get_blocking_keys(df):
    """Private function used to calculate the set of blocking keys

    Calculates the blocking keys simply using the first three characters of the page titles. Each 3-gram extracted in
    this way is a blocking key.

    Args:
        df (pd.DataFrame): The Pandas DataFrame containing specifications and page titles
    Returns:
        blocking_keys (set): The set of blocking keys calculated
    """

    blocking_keys = set()
    for _, row in df.iterrows():
        page_title = row['page_title']
        blocking_key = page_title[:3]
        blocking_keys.add(blocking_key)
    return blocking_keys


# Blocking function: first three chars of the page title
def compute_blocking(df):
    """Function used to compute blocks before the matching phase

    Gets the set of blocking keys and assigns to each specification the first blocking key that will match with the
    corresponding page title.

    Args:
        df (pd.DataFrame): The Pandas DataFrame containing specifications and page titles

    Returns:
        df (pd.DataFrame): The Pandas DataFrame containing specifications, page titles and blocking keys
    """
    print('Computing blocking...')
    blocking_keys = __get_blocking_keys(df)
    df['blocking_key'] = ''
    for index, row in tqdm(df.iterrows()):
        page_title = row['page_title']
        for blocking_key in blocking_keys:
            if blocking_key in page_title:
                df.at[index, 'blocking_key'] = blocking_key
    print(df.head(5))
    print('Blocking computed successfully!')
    print()
    return df


def __get_value_from_index_and_column(df, index, column_name):
    """Private function used to get a value given an index (row) and a column name from a Pandas DataFrame

    Gets the value in the cell of a Pandas DataFrame, identified by a row index and a column name.

    Args:
        df (pd.DataFrame): A Pandas DataFrame
        index (int): Row index of a Pandas DataFrame
        column_name (str): The column name

    Returns:
        value (int, str, obj): The value contained in the cell of the Pandas DataFrame
    """

    row = df.loc[index]
    value = row[column_name]
    return value


def get_pairs_df(df):
    """Function used to get a Pandas DataFrame containing pairs of specifications based on the blocking keys

    Creates a Pandas DataFrame where each row is a pair of specifications. It will create one row for every possible
    combination of specifications inside a block.

    Args:
        df (pd.DataFrame): The Pandas DataFrame containing specifications, page titles and blocking keys

    Returns:
        pairs_df (pd.DataFrame): The Pandas DataFrame containing pairs of specifications
    """
    print('Creating pairs dataframe...\n')
    grouped_df = df.groupby('blocking_key')
    index_pairs = []
    for _, group in grouped_df:
        block_indexes = list(group.index)
        index_pairs.extend(list(itertools.combinations(block_indexes, 2)))

    progressive_id = 0
    progressive_id2row_df = {}
    for index_pair in tqdm(index_pairs):
        left_index, right_index = index_pair
        left_spec_id = __get_value_from_index_and_column(df, left_index, 'spec_id')
        right_spec_id = __get_value_from_index_and_column(df, right_index, 'spec_id')
        left_page_title = __get_value_from_index_and_column(df, left_index, 'page_title')
        right_page_title = __get_value_from_index_and_column(df, right_index, 'page_title')
        row = (left_spec_id, right_spec_id, left_page_title, right_page_title)
        progressive_id2row_df.update({progressive_id: row})
        progressive_id += 1

    columns_df = ['left_spec_id', 'right_spec_id', 'left_page_title', 'right_page_title']
    pairs_df = pd.DataFrame.from_dict(progressive_id2row_df, orient='index', columns=columns_df)
    print(pairs_df.head(5))
    print('Pairs dataframe created successfully!')
    print()
    return pairs_df


# Matching function: two tokens shared
def compute_matching(pairs_df):
    """Function used to actually compute the matching specifications

    Iterates over the pairs DataFrame and uses a matching function to decide if they represent the same real-world
    product or not. Two specifications are matching if they share at least 2 tokens in the page title.
    The tokenization is made by simply splitting strings by using blank character as separetor.

    Args:
        df (pd.DataFrame): The Pandas DataFrame containing pairs of specifications

    Returns:
        matching_pairs_df (pd.DataFrame): The Pandas DataFrame containing the matching pairs
    """

    print('Computing matching...\n')
    columns_df = ['left_spec_id', 'right_spec_id']
    matching_pairs_df = pd.DataFrame(columns=columns_df)
    for index, row in tqdm(pairs_df.iterrows()):
        left_page_title = row['left_page_title']
        right_page_title = row['right_page_title']
        left_tokens = set(left_page_title.split())
        right_tokens = set(right_page_title.split())

        if len(left_tokens.intersection(right_tokens)) >= 2:
            left_spec_id = row['left_spec_id']
            right_spec_id = row['right_spec_id']
            matching_pair_row = pd.Series([left_spec_id, right_spec_id], columns_df)
            matching_pairs_df = matching_pairs_df.append(matching_pair_row, ignore_index=True)
    print(matching_pairs_df.head(5))
    print('Matching computed successfully!')
    print()
    return matching_pairs_df


if __name__ == '__main__':
    print("Start Time: ", end=" ")
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    dataset_df = create_dataframe()
    dataset_df = compute_blocking(dataset_df)
    pairs_df = get_pairs_df(dataset_df)
    matching_pairs_df = compute_matching(pairs_df)
    # Save the submission as CSV file in the OUTPUT_PATH
    matching_pairs_df.to_csv(OUTPUT_PATH + '/submission.csv', index=False)
    print('Submission file created in {} directory.'.format(OUTPUT_PATH))
    print("End Time: ", end=" ")
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
