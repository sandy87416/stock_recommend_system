import pandas as pd
from config import database_path


class ApplicationInformation:
    __account = ''
    __content = ''

    def __init__(self, account, content):
        self.__account = account
        self.__content = content

    def get_account(self):
        return self.__account

    def get_content(self):
        return self.__content

    def set_content(self, content):
        self.__content = content
        self.__save_content_to_database(self.__account, self.__content)

    @staticmethod
    def __save_content_to_database(account, content):
        application_info_df = pd.read_csv(database_path + 'member/application_information.csv')
        application_info_index = application_info_df[application_info_df['account'] == account].index
        application_info_df.iloc[application_info_index, application_info_df.columns.get_loc("content")] = content
        application_info_df.to_csv(database_path + 'member/application_information.csv', index=False)
