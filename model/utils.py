import pandas as pd

from config import database_path


def update_database(path, key_name, key, value_name, value):
    df = pd.read_csv(database_path + path)
    df.iloc[df[df[key_name] == key].index, df.columns.get_loc(value_name)] = value
    df.to_csv(database_path + path, index=False)



