import pandas as pd
from unittest import TestCase
from config import database_path
from model.stock.stock_system import StockSystem


class TestStockSystem(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stock_system = StockSystem()

    def test_create_stock(self):
        stock = self.stock_system.create_stock(2330)
        self.assertEqual(stock.get_stock_id(), 2330)
        self.assertEqual(stock.get_stock_name(), '台積電')
        self.assertEqual(stock.get_stock_company_name(), '台積電')
        self.assertEqual(stock.get_stock_classification(), '半導體業')

    def test_get_stock_after_hours_information(self):
        stock_after_hours_information = self.stock_system.get_stock_after_hours_information(1101)
        self.assertEqual(stock_after_hours_information.get_date(), '2022-04-18')
        self.assertEqual(stock_after_hours_information.get_k_value(), -0.6)
        self.assertEqual(stock_after_hours_information.get_ma20_value(), 49.15)
        self.assertEqual(stock_after_hours_information.get_rsi_value(), 0.0)
        self.assertEqual(stock_after_hours_information.get_foreign_buy(), 3998150.0)
        self.assertEqual(stock_after_hours_information.get_investment_trust_buy(), 1299000.0)
        self.assertEqual(stock_after_hours_information.get_self_buy(), 1142000.0)
        self.assertEqual(stock_after_hours_information.get_news(), '代子公司三元能源科技股份有限公司公告訂購機器設備')
        self.assertEqual(stock_after_hours_information.get_monthly_revenue(), 22037652)

    def test_get_stock_intraday_information(self):
        stock_intraday_information = self.stock_system.get_stock_intraday_information(1101)
        self.assertEqual(stock_intraday_information.get_open_price(), 47.3)
        self.assertEqual(stock_intraday_information.get_high_price(), 47.3)
        self.assertEqual(stock_intraday_information.get_low_price(), 46.5)
        self.assertEqual(stock_intraday_information.get_close_price(), 46.5)

    def test_create_selected_stock(self):
        selected_stock = self.stock_system.create_selected_stock('t109598087@ntut.org.tw', 2330)
        self.assertEqual(selected_stock.get_id(), 't109598087@ntut.org.tw')
        self.assertEqual(selected_stock.get_stock_id(), 2330)

    def test_add_selected_stock(self):
        self.stock_system.add_selected_stock('t109598087@ntut.org.tw', 2330)
        selected_stock_list = self.stock_system.read_selected_stock('t109598087@ntut.org.tw')
        id_list = [selected_stock.get_id() for selected_stock in selected_stock_list]
        stock_id_list = [selected_stock.get_stock_id() for selected_stock in selected_stock_list]
        self.assertTrue('t109598087@ntut.org.tw' in id_list)
        self.assertTrue(2330 in stock_id_list)

        # teardown
        selected_stock_df = pd.read_csv(database_path + 'selected_stock.csv')
        selected_stock_df = selected_stock_df.drop(selected_stock_df[
                                                       (selected_stock_df['id'] == 't109598087@ntut.org.tw') & (
                                                               selected_stock_df['stock_id'] == 2330)].index)
        selected_stock_df.to_csv(database_path + 'selected_stock.csv', index=False)

    def test_get_close_price(self):
        self.assertEqual(self.stock_system.get_close_price(2330), 561.0)

    def test_get_stock_classification(self):
        stock_class_dict = self.stock_system.get_stock_classification()
        self.assertEqual(stock_class_dict['油電燃氣業'][0], '山隆 2616')
