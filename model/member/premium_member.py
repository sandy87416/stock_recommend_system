import pandas as pd

from config import database_path
from model.member.member import Member


class PremiumMember(Member):
    def __init__(self, account, password):
        super().__init__(account, password)
        self.__account = account
        self.__password = password

    def read_stock_odds(self, stock_id):
        now_df = pd.concat(
            [pd.read_csv(database_path + '' + str(days) + 'now.csv') for days in range(2, 10)])
        stock_df = now_df[now_df['stock_id'] == int(stock_id)]
        stock_name = stock_df['stock_name'].to_numpy()[0]

        # print
        to_front_end_message_list = list()
        for i in range(len(stock_df)):
            message = str(stock_id) + stock_name + str(i + 2) + '天賣出' + '勝率:' + str(stock_df['odds'].to_numpy()[i])
            to_front_end_message_list.append(message)

        return to_front_end_message_list
