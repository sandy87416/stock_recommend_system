import pandas as pd

from config import database_path
from model.member.application_information import ApplicationInformation
from model.member.member import Member


class OrdinaryMember(Member):
    def __init__(self, account, password):
        super().__init__(account, password)
        self.__account = account
        self.__password = password
        self.__application_information = self.create_application_information()

    def get_application_information(self):
        return self.__application_information

    def create_application_information(self):
        return ApplicationInformation(self.get_account(), '')

    def apply_premium_member(self, content):
        self.__application_information.set_content(content)
        return 'Success'
