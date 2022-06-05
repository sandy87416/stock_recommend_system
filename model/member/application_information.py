import pandas as pd
from config import database_path


class ApplicationInformation:
    __id = ''
    __content = ''

    def __init__(self, id, content):
        self.__id = id
        self.__content = content

    def get_id(self):
        return self.__id

    def get_content(self):
        return self.__content

    def set_content(self, content):
        self.__content = content

    def create_content_to_database(self):
        df = pd.read_csv(database_path + 'member/application_information.csv')
        df = pd.concat([df, pd.DataFrame({
            'id': [self.__id],
            'content': [self.__content],
        })])
        df.to_csv(database_path + 'member/application_information.csv', index=False)
