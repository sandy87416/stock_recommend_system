import pandas as pd

from config import database_path
from model.member.member import Member


class PremiumMember(Member):
    def __init__(self, account, password):
        super().__init__(account, password)
        self.__account = account
        self.__password = password
        member_df = pd.read_csv(database_path + 'member/member.csv')
        member_df = pd.concat([member_df, pd.DataFrame({
            'account': [account],
            'password': [password],
            'level': [1],
        })])
        member_df.to_csv(database_path + 'member/member.csv', index=False)

    def read_recommended_stock(self, days, odds):
        days = int(days)
        odds = float(odds) / 10

        very_good_df = pd.read_csv(database_path + '' + str(days) + 'now.csv')
        # send_to_line
        very_good_df = very_good_df[(very_good_df['odds'] > odds)]  # 可修改

        # print(very_good_df['stock_name'])
        # print(very_good_df)
        very_good_df = very_good_df.sort_values('odds', ascending=False)

        # print
        to_front_end_message_list = list()
        very_good_stock_id_np = very_good_df['stock_id'].to_numpy()
        very_good_stock_stock_name_np = very_good_df['stock_name'].to_numpy()
        very_good_stock_rsi_np = very_good_df['rsi_6'].to_numpy()
        very_good_stock_win_rate_np = very_good_df['odds'].to_numpy()
        for i in range(len(very_good_df)):
            print_str = ''
            # print(very_good_stock_is_up_stop_np[i])
            # if very_good_stock_is_up_stop_np[i] == 1:
            #     print_str += '[漲停]'
            print_str += str(very_good_stock_id_np[i])
            print_str += very_good_stock_stock_name_np[i] + ' '
            print_str += 'rsi_6:' + str(very_good_stock_rsi_np[i]) + ' '
            print_str += 'win_rate:' + str(round(very_good_stock_win_rate_np[i], 2))
            to_front_end_message_list.append(print_str)
        return to_front_end_message_list

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
