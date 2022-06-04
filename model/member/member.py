import pandas as pd
from config import database_path
from model import stock_system
from model.stock.calculator import Calculator


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
        stock_after_hours_information = stock_system.get_stock_after_hours_information(stock_id)
        return stock_after_hours_information

    @staticmethod
    def read_stock_intraday_information(stock_id):
        stock_intraday_information = stock_system.get_stock_intraday_information(stock_id)
        return stock_intraday_information

    def add_selected_stock(self, stock_id):
        selected_stock_list = stock_system.add_selected_stock(self.get_account(), stock_id)
        return selected_stock_list

    def read_selected_stock(self):
        selected_stock_list = stock_system.read_selected_stock(self.get_account())
        return selected_stock_list

    def delete_selected_stock(self, stock_id):
        selected_stock_list = stock_system.delete_selected_stock(self.get_account(), stock_id)
        return selected_stock_list

    @staticmethod
    def calculate_current_profit_and_loss(stock_id, buy_price, trading_volume, securities_firm):
        close_price = stock_system.get_close_price(stock_id)
        calculator = Calculator()
        return calculator.calculate_profit_and_loss(buy_price, close_price, trading_volume, securities_firm)

    @staticmethod
    def calculate_profit_and_loss(buy_price, sell_price, trading_volume, securities_firm):
        calculator = Calculator()
        return calculator.calculate_profit_and_loss(buy_price, sell_price, trading_volume, securities_firm)

    @staticmethod
    def read_stock_classification():
        return stock_system.get_stock_classification()
