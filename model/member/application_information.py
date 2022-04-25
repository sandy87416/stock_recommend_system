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
