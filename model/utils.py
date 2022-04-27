import pandas as pd

from config import database_path


def update_database(path, key_name, key, value_name, value):
    member_df = pd.read_csv(database_path + path)
    member_df.iloc[member_df[member_df[key_name] == key].index, member_df.columns.get_loc(value_name)] = value
    member_df.to_csv(database_path + path, index=False)
