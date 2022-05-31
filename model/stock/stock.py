import pandas as pd
from config import database_path
from model.stock.after_hours_information import AfterHoursInformation
from model.stock.calculator import Calculator
from model.stock.intraday_information import IntraDayInformation


class Stock:
    __stock_id = 0
    __stock_name = ''
    __stock_company_name = ''
    __stock_classification = ''
    __stock_intraday_information = ''
    __stock_after_hours_information = ''

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

    @staticmethod
    def create_stock_after_hours_information(stock_id):
        stock_df = pd.read_csv(database_path + '' + str(stock_id) + '.csv')
        close_price_np = stock_df['Close'].to_numpy()
        calculator = Calculator()
        rsi_list = calculator.get_rsi_list(close_price_np, 6)
        # rsi_value
        rsi_value = rsi_list[-1]
        # date
        date = stock_df['Date'].to_numpy()[-1]
        # k
        k_value = calculator.get_up_down_list(close_price_np)[-1]
        # ma20_value
        ma20_value = calculator.get_mean_price_list(close_price_np, 20)[-1]

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
