import numpy as np
import pandas as pd

from config import database_path
from joblib import load


class Calculator:
    def __init__(self):
        pass

    @staticmethod
    def __get_up_down_list(end_price_list):
        return [0] + [end_price_list[i] - end_price_list[i - 1] for i in range(1, len(end_price_list))]

    @staticmethod
    def __get_rsi(days_up_down_list):
        up_mean = np.sum([up_down for up_down in days_up_down_list if up_down > 0])
        down_mean = -np.sum([up_down for up_down in days_up_down_list if up_down < 0])
        return round(up_mean / (up_mean + down_mean) * 100, 2)

    def __get_rsi_list(self, end_price_list, days):
        rsi_list = [0 for _ in range(days - 1)]
        for i in range(len(end_price_list) - (days - 1)):
            days_end_price_list = end_price_list[i:(i + days)]
            days_up_down_list = self.__get_up_down_list(days_end_price_list)
            rsi = self.__get_rsi(days_up_down_list)
            rsi_list.append(rsi)
        return rsi_list

    @staticmethod
    def __get_corr(end_day_end_point, start_day_end_point, days):
        return round(((end_day_end_point - start_day_end_point) / end_day_end_point) / days, 6)

    def __get_corr_list(self, end_price_list, days):
        corr_list = [0 for _ in range(days - 1)]
        for i in range(len(end_price_list) - (days - 1)):
            days_end_price_list = end_price_list[i:(i + days)]
            corr_list.append(self.__get_corr(days_end_price_list[-1], days_end_price_list[0], days))
        return corr_list

    @staticmethod
    def calculate_profit_and_loss(buy_price, sell_price, trading_volume=1000, securities_firm=0.6):
        fee = (0.1425 / 100) * securities_firm
        tax = 0.3 / 100
        fee_and_tax = (buy_price * fee + sell_price * tax + sell_price * fee)
        return round((sell_price - buy_price - fee_and_tax) * trading_volume)

    def read_recommended_stock(self, days=5, odds=0.7):
        stock_df = pd.read_csv(database_path + 'now.csv')
        stock_id_name_df = pd.read_csv(database_path + 'stock_id_table.csv')
        all_stock_id_np = stock_id_name_df['stock_id'].to_numpy()

        all_company_df_dict = {stock_id: pd.read_csv(database_path + str(stock_id) + '.csv') for stock_id in
                               all_stock_id_np}

        areal_now_df = pd.DataFrame()
        areal_now_df['stock_id'] = stock_df['代號▼']
        areal_now_df['Open'] = stock_df['昨收▼']
        areal_now_df['High'] = stock_df['最高▼']
        areal_now_df['Low'] = stock_df['最低▼']
        areal_now_df['Close'] = stock_df['價格▼']
        areal_now_df['stock_name'] = stock_df['名稱▼']

        for stock_id in all_stock_id_np:
            stock_id_df = all_company_df_dict[stock_id]
            stock_id_df = pd.concat([stock_id_df, areal_now_df[areal_now_df['stock_id'] == str(stock_id)]])
            all_company_df_dict[stock_id] = stock_id_df

        for stock_id in all_stock_id_np:
            stock_id_df = all_company_df_dict[stock_id]
            stock_id_df['corr_20'] = self.__get_corr_list(stock_id_df['Close'].to_numpy(), 20)
            stock_id_df['rsi_6'] = self.__get_rsi_list(stock_id_df['Close'].to_numpy(), 6)
            stock_id_df['stock_id'] = [stock_id] * len(stock_id_df)
            all_company_df_dict[stock_id] = stock_id_df

        all_stock_last_day_df = pd.concat([all_company_df_dict[stock_id].tail(1) for stock_id in all_stock_id_np])
        stock_df = all_stock_last_day_df

        stock_df = stock_df.sort_values('corr_20', ascending=False)
        stock_df['corr_20_rank'] = [i for i in range(len(stock_df['stock_id']))]

        stock_df = stock_df[['stock_id', 'stock_name'] + ['Open', 'High', 'Low', 'Close', 'rsi_6']]
        stock_df = stock_df.dropna()
        to_front_end_message_list = self.__calculate_recommended_stock(days, odds, stock_df)

        return to_front_end_message_list

    @staticmethod
    def __calculate_recommended_stock(days, odds, now_df):
        # get_odds from train
        X_test = now_df[['Open', 'High', 'Low', 'Close', 'rsi_6']].values
        clf = load(database_path + str(days) + 'RandomForest.joblib')
        a_list = clf.predict_proba(X_test)
        now_df['odds'] = [a[1] for a in a_list]

        now_df['Open'] = now_df['Open'].astype('float32')
        now_df['High'] = now_df['High'].astype('float32')
        now_df['Low'] = now_df['Low'].astype('float32')
        now_df['Close'] = now_df['Close'].astype('float32')

        ################################

        now_df = now_df[(now_df['odds'] > odds)]  # 可修改

        now_df = now_df.sort_values('odds', ascending=False)

        # print
        to_front_end_message_list = list()
        very_good_stock_id_np = now_df['stock_id'].to_numpy()
        very_good_stock_stock_name_np = now_df['stock_name'].to_numpy()
        very_good_stock_rsi_np = now_df['rsi_6'].to_numpy()
        very_good_stock_win_rate_np = now_df['odds'].to_numpy()
        for i in range(len(now_df)):
            print_str = ''
            print_str += str(very_good_stock_id_np[i])
            print_str += very_good_stock_stock_name_np[i] + ' '
            print_str += 'rsi_6:' + str(very_good_stock_rsi_np[i]) + ' '
            print_str += 'win_rate:' + str(round(very_good_stock_win_rate_np[i], 2))
            to_front_end_message_list.append(print_str)
        return to_front_end_message_list
