import pandas as pd

from config import database_path


class Admin:
    __account = ''
    __password = ''

    def __init__(self, account, password):
        self.__account = account
        self.__password = password

    def get_account(self):
        return self.__account

    def get_password(self):
        return self.__password

    @staticmethod
    def __save_password_to_database(account, password):
        member_df = pd.read_csv(database_path + 'member/member.csv')
        member_index = member_df[member_df['account'] == account].index
        member_df.iloc[member_index, member_df.columns.get_loc("password")] = password
        member_df.to_csv(database_path + 'member/member.csv', index=False)

    def set_password(self, password):
        self.__password = password
        self.__save_password_to_database(self.__account, self.__password)

    @staticmethod
    def upgrade_member_level(account):
        member_df = pd.read_csv(database_path + 'member/member.csv')
        level = member_df[member_df['account'] == account]['level'].to_numpy()[0]
        if level == 2:
            member_df.iloc[member_df[member_df['account'] == account].index, member_df.columns.get_loc("level")] = 1
        member_df.to_csv(database_path + 'member/member.csv', index=False)
