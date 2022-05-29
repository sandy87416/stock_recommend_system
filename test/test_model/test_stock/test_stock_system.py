from unittest import TestCase

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
