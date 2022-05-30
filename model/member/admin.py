import pandas as pd

from config import database_path
from model.utils import update_database


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

    def set_password(self, password):
        self.__password = password
        update_database('member/member.csv', 'account', self.__account, "password", self.__password)

    @staticmethod
    def upgrade_member_level(account):
        member_df = pd.read_csv(database_path + 'member/member.csv')
        level = member_df[member_df['account'] == account]['level'].to_numpy()[0]
        if level == 2:
            member_df.iloc[member_df[member_df['account'] == account].index, member_df.columns.get_loc("level")] = 1
        member_df.to_csv(database_path + 'member/member.csv', index=False)

        # delete application_information data
        application_information_df = pd.read_csv(database_path + 'member/application_information.csv')
        application_information_df['account'] = application_information_df['account'].astype('str')
        application_information_df = application_information_df.drop(
            application_information_df[application_information_df['account'] == account].index)
        application_information_df.to_csv(database_path + 'member/application_information.csv', index=False)

    @staticmethod
    def get_application_information_zip():
        application_information_df = pd.read_csv(database_path + 'member/application_information.csv')
        return zip(application_information_df['account'].to_list(), application_information_df['content'].to_list())
