import pandas as pd

from config import database_path


class Calculator:

    def __init__(self):
        pass

    @staticmethod
    def calculate_profit_and_loss(buy_price, sell_price, trading_volume=1000, securities_firm=0.6):
        fee = (0.1425 / 100) * securities_firm
        tax = 0.3 / 100
        fee_and_tax = (buy_price * fee + sell_price * tax + sell_price * fee)
        return round((sell_price - buy_price - fee_and_tax) * trading_volume)

    def read_recommended_stock(self, days, odds):
        days = int(days)
        odds = float(odds) / 10

        very_good_df = pd.read_csv(database_path + '' + str(days) + 'now.csv')
        # send_to_line
        very_good_df = very_good_df[(very_good_df['odds'] > odds)]  # 可修改

        very_good_df = very_good_df.sort_values('odds', ascending=False)

        # print
        to_front_end_message_list = list()
        very_good_stock_id_np = very_good_df['stock_id'].to_numpy()
        very_good_stock_stock_name_np = very_good_df['stock_name'].to_numpy()
        very_good_stock_rsi_np = very_good_df['rsi_6'].to_numpy()
        very_good_stock_win_rate_np = very_good_df['odds'].to_numpy()
        for i in range(len(very_good_df)):
            print_str = ''
            print_str += str(very_good_stock_id_np[i])
            print_str += very_good_stock_stock_name_np[i] + ' '
            print_str += 'rsi_6:' + str(very_good_stock_rsi_np[i]) + ' '
            print_str += 'win_rate:' + str(round(very_good_stock_win_rate_np[i], 2))
            to_front_end_message_list.append(print_str)
        return to_front_end_message_list
