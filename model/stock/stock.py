import pandas as pd
import numpy as np

from config import database_path

from model.stock.after_hours_information import AfterHoursInformation
from model.stock.intra_day_information import IntraDayInformation


def is_nan(num):
    return num != num


def get_rsi(days_up_down_list):
    up_mean = np.sum([up_down for up_down in days_up_down_list if up_down > 0])
    down_mean = -np.sum([up_down for up_down in days_up_down_list if up_down < 0])
    return round(up_mean / (up_mean + down_mean) * 100, 2)


def get_mean_price_list(end_price_list, days):
    mean_price_list = [0 for _ in range(days - 1)]
    for i in range(len(end_price_list) - (days - 1)):
        days_end_price_list = end_price_list[i:(i + days)]
        mean_price_list.append(round(np.mean(days_end_price_list) + 0, 2))
    return mean_price_list


class Stock:
    __stock_id = 0
    __stock_name = ''
    __stock_company_name = ''
    __stock_classification = ''

    def __init__(self, stock_id, stock_name, stock_company_name, stock_classification):
        self.__stock_id = stock_id
        self.__stock_name = stock_name
        self.__stock_company_name = stock_company_name
        self.__stock_classification = stock_classification

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

    @staticmethod
    def get_stock_after_hours_information(stock_id):
        df = pd.read_csv(database_path + '' + str(stock_id) + '.csv')
        df = df.sort_values(['Date'], ascending=[False])
        news_df = pd.read_csv(database_path + 'news.csv')
        news_df = news_df.sort_values(['date', 'time'], ascending=[False, False])
        news_list = news_df[news_df['stock_id'] == stock_id].to_numpy()
        monthly_revenue_df = pd.read_csv(database_path + 'month_revenue.csv')
        monthly_revenue_df = monthly_revenue_df[monthly_revenue_df['stock_id'] == stock_id]

        date = df['Date'].to_numpy()[0]
        k_value = ''
        ma20_value = get_mean_price_list(df['Close'].to_numpy(), 20)[0]
        rsi_value = get_rsi(df['Close'].to_numpy())
        foreign_buy = '0' if is_nan(df['foreign_buy'].to_numpy()[0]) else df['foreign_buy'].to_numpy()[0]
        investment_trust_buy = '0' if is_nan(df['investment_trust_buy'].to_numpy()[0]) else \
            df['investment_trust_buy'].to_numpy()[0]
        self_buy = '0' if is_nan(df['self_buy'].to_numpy()[0]) else df['self_buy'].to_numpy()[0]
        news = news_list[0] if len(news_list) >= 1 else ''
        monthly_revenue = monthly_revenue_df['month_revenue'].to_numpy()[0]
        after_hours_information = AfterHoursInformation(date, k_value, ma20_value, rsi_value, foreign_buy,
                                                        investment_trust_buy, self_buy, news, monthly_revenue)
        return after_hours_information

    @staticmethod
    def get_stock_intraday_information(stock_id):
        df = pd.read_csv(database_path + '' + str(stock_id) + '.csv')
        df = df.sort_values(by="Date", ascending=[False])
        end_price = round(df['Close'].to_numpy()[0], 2)
        min_price = round(df['Low'].to_numpy()[0], 2)
        max_price = round(df['High'].to_numpy()[0], 2)
        start_price = round(df['Open'].to_numpy()[0], 2)
        intraday_information = IntraDayInformation(end_price, min_price, max_price, start_price)
        return intraday_information

    @staticmethod
    def create_stock_intraday_information(stock_id):
        df = pd.read_csv(database_path + str(stock_id) + '.csv')
        df = df.sort_values(by="Date", ascending=[False])
        end_price = round(df['Close'].to_numpy()[0], 2)
        min_price = round(df['Low'].to_numpy()[0], 2)
        max_price = round(df['High'].to_numpy()[0], 2)
        start_price = round(df['Open'].to_numpy()[0], 2)
        return IntraDayInformation(end_price, min_price, max_price, start_price)

    @staticmethod
    def get_end_price(stock_id):
        df = pd.read_csv(database_path + str(stock_id) + '.csv')
        df = df.sort_values(by="Date", ascending=[False])
        end_price = round(df['Close'].to_numpy()[0], 2)
        return end_price
