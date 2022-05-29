import pandas as pd

from config import database_path
from model.stock.stock_system import StockSystem


class Member:
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
        member_df = pd.read_csv(database_path + 'member/member.csv')
        member_df.iloc[member_df[member_df['account'] == self.get_account()].index, member_df.columns.get_loc(
            "password")] = password
        member_df.to_csv(database_path + 'member/member.csv', index=False)

    @staticmethod
    def read_stock_after_hours_information(stock_id):
        stock_system = StockSystem()
        stock_after_hours_information = stock_system.get_stock_after_hours_information(stock_id)
        return stock_after_hours_information

    @staticmethod
    def read_stock_intraday_information(stock_id):
        stock_system = StockSystem()
        stock_intraday_information = stock_system.get_stock_intraday_information(stock_id)
        return stock_intraday_information
