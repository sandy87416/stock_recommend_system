import numpy as np
import pandas as pd

from config import database_path
from joblib import load


class Calculator:
    def __init__(self):
        pass

    @staticmethod
    def get_mean_price_list(close_price_list, days):
        mean_price_list = [0 for _ in range(days - 1)]
        for i in range(len(close_price_list) - (days - 1)):
            days_close_price_list = close_price_list[i:(i + days)]
            mean_price_list.append(round(np.mean(days_close_price_list) + 0, 2))
        return mean_price_list

    @staticmethod
    def get_up_down_list(close_price_list):
        return [0] + [round(close_price_list[i] - close_price_list[i - 1], 2) for i in range(1, len(close_price_list))]

    @staticmethod
    def __get_rsi(days_up_down_list):
        up_mean = np.sum([up_down for up_down in days_up_down_list if up_down > 0])
        down_mean = -np.sum([up_down for up_down in days_up_down_list if up_down < 0])
        return round(up_mean / (up_mean + down_mean) * 100, 2)

    def get_rsi_list(self, close_price_list, days):
        rsi_list = [0 for _ in range(days - 1)]
        for i in range(len(close_price_list) - (days - 1)):
            days_close_price_list = close_price_list[i:(i + days)]
            days_up_down_list = self.get_up_down_list(days_close_price_list)
            rsi = self.__get_rsi(days_up_down_list)
            rsi_list.append(rsi)
        return rsi_list

    @staticmethod
    def __get_corr(end_day_end_point, start_day_end_point, days):
        return round(((end_day_end_point - start_day_end_point) / end_day_end_point) / days, 6)

    def __get_corr_list(self, close_price_list, days):
        corr_list = [0 for _ in range(days - 1)]
        for i in range(len(close_price_list) - (days - 1)):
            days_close_price_list = close_price_list[i:(i + days)]
            corr_list.append(self.__get_corr(days_close_price_list[-1], days_close_price_list[0], days))
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
            stock_id_df['rsi_6'] = self.get_rsi_list(stock_id_df['Close'].to_numpy(), 6)
            stock_id_df['stock_id'] = [stock_id] * len(stock_id_df)
            all_company_df_dict[stock_id] = stock_id_df

        all_stock_last_day_df = pd.concat([all_company_df_dict[stock_id].tail(1) for stock_id in all_stock_id_np])
        stock_df = all_stock_last_day_df

        stock_df = stock_df.sort_values('corr_20', ascending=False)
        stock_df['corr_20_rank'] = [i for i in range(len(stock_df['stock_id']))]

        stock_df = stock_df[['stock_id', 'stock_name'] + ['Open', 'High', 'Low', 'Close', 'rsi_6']]
        stock_df = stock_df.dropna()
        recommended_stock_list = self.__calculate_recommended_stock(days, odds, stock_df)
        return recommended_stock_list

    @staticmethod
    def __calculate_recommended_stock(days, odds, stock_df):
        x_test = stock_df[['Open', 'High', 'Low', 'Close', 'rsi_6']].values
        clf = load(database_path + str(days) + 'RandomForest.joblib')
        a_list = clf.predict_proba(x_test)
        stock_df['odds'] = [a[1] for a in a_list]

        stock_df['Open'] = stock_df['Open'].astype('float32')
        stock_df['High'] = stock_df['High'].astype('float32')
        stock_df['Low'] = stock_df['Low'].astype('float32')
        stock_df['Close'] = stock_df['Close'].astype('float32')

        stock_df = stock_df[(stock_df['odds'] > odds)]  # 可修改

        stock_df = stock_df.sort_values('odds', ascending=False)

        # print
        very_good_stock_id_np = stock_df['stock_id'].to_numpy()
        very_good_stock_stock_name_np = stock_df['stock_name'].to_numpy()
        very_good_stock_rsi_np = stock_df['rsi_6'].to_numpy()
        very_good_stock_win_rate_np = stock_df['odds'].to_numpy()

        recommended_stock_list = [{'stock_id': str(very_good_stock_id_np[i]),
                                   'stock_name': very_good_stock_stock_name_np[i],
                                   'rsi_6': str(very_good_stock_rsi_np[i]),
                                   'odds': str(round(very_good_stock_win_rate_np[i], 2))
                                   }
                                  for i in range(len(stock_df))]
        return recommended_stock_list

    @staticmethod
    def __calculate_stock_odds(stock_df):
        x_test = stock_df[['Open', 'High', 'Low', 'Close', 'rsi_6']].values

        odds_df = pd.DataFrame()
        for days in range(2, 10):
            clf = load(database_path + str(days) + 'RandomForest.joblib')
            a_list = clf.predict_proba(x_test)

            stock_df['odds'] = [a[1] for a in a_list]
            stock_df['Open'] = stock_df['Open'].astype('float32')
            stock_df['High'] = stock_df['High'].astype('float32')
            stock_df['Low'] = stock_df['Low'].astype('float32')
            stock_df['Close'] = stock_df['Close'].astype('float32')
            odds_df = pd.concat([odds_df, stock_df])

        odds_df = odds_df.sort_values('odds', ascending=False)
        stock_id_name_df = pd.read_csv(database_path + 'stock_id_table.csv')
        stock_id = odds_df['stock_id'].to_numpy()[0]
        stock_name = stock_id_name_df[stock_id_name_df['stock_id'] == stock_id]['stock_name'].to_numpy()[0]
        # print
        stock_odds_list = [{'stock_id': str(stock_id),
                            'stock_name': stock_name,
                            'days': str(i + 2),
                            'odds': str(round(odds_df['odds'].to_numpy()[i], 2))
                            }
                           for i in range(len(odds_df))]
        return stock_odds_list

    def read_stock_odds(self, stock_id):
        stock_df = pd.read_csv(database_path + 'now.csv')
        stock_df = stock_df[stock_df['代號▼'] == str(stock_id)]

        all_company_df_dict = {stock_id: pd.read_csv(database_path + str(stock_id) + '.csv')}

        areal_now_df = pd.DataFrame()
        areal_now_df['stock_id'] = stock_df['代號▼']
        areal_now_df['Open'] = stock_df['昨收▼']
        areal_now_df['High'] = stock_df['最高▼']
        areal_now_df['Low'] = stock_df['最低▼']
        areal_now_df['Close'] = stock_df['價格▼']
        areal_now_df['stock_name'] = stock_df['名稱▼']

        stock_id_df = all_company_df_dict[stock_id]
        stock_id_df = pd.concat([stock_id_df, areal_now_df[areal_now_df['stock_id'] == str(stock_id)]])
        all_company_df_dict[stock_id] = stock_id_df

        stock_id_df['corr_20'] = self.__get_corr_list(stock_id_df['Close'].to_numpy(), 20)
        stock_id_df['rsi_6'] = self.get_rsi_list(stock_id_df['Close'].to_numpy(), 6)
        stock_id_df['stock_id'] = [stock_id] * len(stock_id_df)
        all_company_df_dict[stock_id] = stock_id_df

        all_stock_last_day_df = pd.concat([all_company_df_dict[stock_id].tail(1)])
        stock_df = all_stock_last_day_df

        stock_df = stock_df.sort_values('corr_20', ascending=False)
        stock_df['corr_20_rank'] = [i for i in range(len(stock_df['stock_id']))]

        stock_df = stock_df[['stock_id', 'stock_name'] + ['Open', 'High', 'Low', 'Close', 'rsi_6']]
        stock_df = stock_df.dropna()
        stock_odds_list = self.__calculate_stock_odds(stock_df)
        return stock_odds_list
