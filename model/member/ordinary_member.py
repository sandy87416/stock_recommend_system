import pandas as pd

from config import database_path
from model.member.application_information import ApplicationInformation
from model.member.member import Member


class OrdinaryMember(Member):
    def __init__(self, id, password):
        super().__init__(id, password)
        self.__id = id
        self.__password = password
        self.__application_information = ApplicationInformation(self.get_id(), '')

    def get_application_information(self):
        return self.__application_information

    def apply_premium_member(self, content):
        self.__application_information.set_content(content)
        self.__application_information.create_content_to_database()

    def get_apply_content(self):
        application_information_df = pd.read_csv(database_path + 'member/application_information.csv')
        application_information_df['content'] = application_information_df['content'].astype('str')
        application_information_df['id'] = application_information_df['id'].astype('str')
        application_information_df = application_information_df[application_information_df['id'] == self.get_id()]
        if len(application_information_df['content'].to_numpy()) != 0:
            return application_information_df['content'].to_numpy()[0]
        else:
            return ''
