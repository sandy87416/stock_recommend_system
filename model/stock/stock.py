import pandas as pd
import numpy as np

from config import database_path

from model.stock.after_hours_information import AfterHoursInformation
from model.stock.intraday_information import IntraDayInformation


class Stock:
    __stock_id = 0
    __stock_name = ''
    __stock_company_name = ''
    __stock_classification = ''
    __stock_intraday_information = ''
    __stock_after_hours_information = ''

    @staticmethod
    def __get_up_down_list(close_price_list):
        return [0] + [round(close_price_list[i] - close_price_list[i - 1], 2) for i in range(1, len(close_price_list))]

    # https://wiki.mbalib.com/zh-tw/%E7%9B%B8%E5%AF%B9%E5%BC%BA%E5%BC%B1%E6%8C%87%E6%A0%87

    @staticmethod
    def __get_rsi(days_up_down_list):
        up_mean = np.sum([up_down for up_down in days_up_down_list if up_down > 0])
        down_mean = -np.sum([up_down for up_down in days_up_down_list if up_down < 0])
        return round(up_mean / (up_mean + down_mean) * 100, 2)

    def __get_rsi_list(self, close_price_list, days):  # todo: calculator?
        rsi_list = [0 for _ in range(days - 1)]
        for i in range(len(close_price_list) - (days - 1)):
            days_close_price_list = close_price_list[i:(i + days)]
            days_up_down_list = self.__get_up_down_list(days_close_price_list)
            rsi = self.__get_rsi(days_up_down_list)
            rsi_list.append(rsi)
        return rsi_list

    @staticmethod
    def __get_mean_price_list(close_price_list, days):
        mean_price_list = [0 for _ in range(days - 1)]
        for i in range(len(close_price_list) - (days - 1)):
            days_close_price_list = close_price_list[i:(i + days)]
            mean_price_list.append(round(np.mean(days_close_price_list) + 0, 2))
        return mean_price_list

    def __init__(self, stock_id, stock_name, stock_company_name, stock_classification):
        self.__stock_id = stock_id
        self.__stock_name = stock_name
        self.__stock_company_name = stock_company_name
        self.__stock_classification = stock_classification
        self.__stock_intraday_information = self.create_stock_intraday_information(stock_id)
        self.__stock_after_hours_information = self.create_stock_after_hours_information(stock_id)

    def get_stock_id(self):
        return self.__stock_id

    def set_stock_id(self, stock_id):
        self.__stock_id = stock_id

    def get_stock_name(self):
        return self.__stock_name

    def set_stock_name(self, stock_name):
        self.__stock_name = stock_name

    def get_stock_company_name(self):
        return self.__stock_company_name

    def set_stock_company_name(self, stock_company_name):
        self.__stock_company_name = stock_company_name

    def get_stock_classification(self):
        return self.__stock_classification

    def set_stock_classification(self, stock_classification):
        self.__stock_classification = stock_classification

    def get_stock_intraday_information(self):
        return self.__stock_intraday_information

    def get_stock_after_hours_information(self):
        return self.__stock_after_hours_information

    @staticmethod
    def create_stock_intraday_information(stock_id):
        # # new
        # now_df = pd.read_html('https://histock.tw/stock/rank.aspx?p=all')[0]
        # now_df = now_df[now_df['代號▼'] == str(stock_id)]
        # open_price = round(now_df['昨收▼'].to_numpy()[0], 2)
        # high_price = round(now_df['最高▼'].to_numpy()[0], 2)
        # low_price = round(now_df['最低▼'].to_numpy()[0], 2)
        # close_price = round(now_df['價格▼'].to_numpy()[0], 2)
        # old
        df = pd.read_csv(database_path + str(stock_id) + '.csv')
        df_tail = df.tail(1)
        open_price = round(df_tail['Open'].to_numpy()[0], 2)
        high_price = round(df_tail['High'].to_numpy()[0], 2)
        low_price = round(df_tail['Low'].to_numpy()[0], 2)
        close_price = round(df_tail['Close'].to_numpy()[0], 2)
        return IntraDayInformation(open_price, high_price, low_price, close_price)

    def create_stock_after_hours_information(self, stock_id):
        stock_df = pd.read_csv(database_path + '' + str(stock_id) + '.csv')
        close_price_np = stock_df['Close'].to_numpy()
        rsi_list = self.__get_rsi_list(close_price_np, 6)
        # rsi_value
        rsi_value = rsi_list[-1]
        # date
        date = stock_df['Date'].to_numpy()[-1]
        # k
        k_value = self.__get_up_down_list(close_price_np)[-1]
        # ma20_value
        ma20_value = self.__get_mean_price_list(close_price_np, 20)[-1]

        foreign_buy = stock_df['foreign_buy'].to_numpy()[-1]
        investment_trust_buy = stock_df['investment_trust_buy'].to_numpy()[-1]
        self_buy = stock_df['self_buy'].to_numpy()[-1]

        # news
        news_df = pd.read_csv(database_path + 'news.csv')
        news_list = news_df[news_df['stock_id'] == stock_id]['company_news'].to_numpy()
        news = news_list[0] if len(news_list) >= 1 else ''

        # monthly_revenue
        monthly_revenue_df = pd.read_csv(database_path + 'month_revenue.csv')
        monthly_revenue_df = monthly_revenue_df[monthly_revenue_df['stock_id'] == stock_id]
        monthly_revenue = monthly_revenue_df['month_revenue'].to_numpy()[0]

        after_hours_information = AfterHoursInformation(date, k_value, ma20_value, rsi_value, foreign_buy,
                                                        investment_trust_buy, self_buy, news, monthly_revenue)
        return after_hours_information
