import pandas as pd
from flask_login import UserMixin
from config import database_path
from model.member.application_information import ApplicationInformation
from model.utils import update_database


class Admin(UserMixin):
    __id = ''
    __password = ''

    def __init__(self, id, password):
        self.__id = id
        self.__password = password

    def get_id(self):
        return self.__id

    def get_password(self):
        return self.__password

    def set_password(self, password):
        self.__password = password
        update_database('member/member.csv', 'id', self.__id, "password", self.__password)

    @staticmethod
    def __upgrade(id):
        member_df = pd.read_csv(database_path + 'member/member.csv')
        level = member_df[member_df['id'] == id]['level'].to_numpy()[0]
        if level == 2:
            member_df.iloc[member_df[member_df['id'] == id].index, member_df.columns.get_loc("level")] = 1
        member_df.to_csv(database_path + 'member/member.csv', index=False)

    @staticmethod
    def delete_application_information_data(id):
        application_information_df = pd.read_csv(database_path + 'member/application_information.csv')
        application_information_df['id'] = application_information_df['id'].astype('str')
        application_information_df = application_information_df.drop(
            application_information_df[application_information_df['id'] == id].index)
        application_information_df.to_csv(database_path + 'member/application_information.csv', index=False)

    def upgrade_member_level(self, id):
        self.__upgrade(id)
        self.delete_application_information_data(id)
        return self.get_application_information_list()

    @staticmethod
    def get_application_information_list():
        application_information_df = pd.read_csv(database_path + 'member/application_information.csv')
        application_information_df['content'] = application_information_df['content'].astype('str')
        id_np = application_information_df['id'].to_numpy()
        content_np = application_information_df['content'].to_numpy()
        return [ApplicationInformation(id_np[i], content_np[i]) for i in range(len(id_np))]
