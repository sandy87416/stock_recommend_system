import pandas as pd

from config import database_path
from model.member.application_information import ApplicationInformation
from model.member.member import Member
from model.utils import update_database


class OrdinaryMember(Member):
    def __init__(self, account, password):
        super().__init__(account, password)
        self.__account = account
        self.__password = password
        self.__application_information = None

    def create_application_information(self):
        self.__application_information = ApplicationInformation(self.get_account(), '')

    def apply_premium_member(self, content):
        self.__application_information.set_content(content)
        apply_account = self.__application_information.get_account()
        apply_content = self.__application_information.get_content()

        df = pd.read_csv(database_path + 'member/application_information.csv')
        df = pd.concat([df, pd.DataFrame({
            'account': [apply_account],
            'content': [apply_content],
        })])
        df.to_csv(database_path + 'member/application_information.csv', index=False)
        return 'Success'

    def get_application_information(self):
        return self.__application_information
