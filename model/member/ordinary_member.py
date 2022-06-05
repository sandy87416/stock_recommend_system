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
