from unittest import TestCase

from model.stock.stock import Stock


class TestStock(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stock = Stock(1101, '台泥', '台灣水泥', '水泥工業')

    def test_get_stock_id(self):
        self.assertEqual(self.stock.get_stock_id(), 1101)

    def test_set_stock_id(self):
        self.stock.set_stock_id(1102)
        self.assertEqual(self.stock.get_stock_id(), 1102)

    def test_get_stock_name(self):
        self.assertEqual(self.stock.get_stock_name(), '台泥')

    def test_set_stock_name(self):
        self.stock.set_stock_name('亞泥')
        self.assertEqual(self.stock.get_stock_name(), '亞泥')

    def test_get_stock_company_name(self):
        self.assertEqual(self.stock.get_stock_company_name(), '台灣水泥')

    def test_set_stock_company_name(self):
        self.stock.set_stock_company_name('亞洲水泥')
        self.assertEqual(self.stock.get_stock_company_name(), '亞洲水泥')

    def test_get_stock_classification(self):
        self.assertEqual(self.stock.get_stock_classification(), '水泥工業')

    def test_set_stock_classification(self):
        self.stock.set_stock_classification('食品工業')
        self.assertEqual(self.stock.get_stock_classification(), '食品工業')

    def test_create_stock_after_hours_information(self):
        after_hours_information = self.stock.create_stock_after_hours_information(1215)
        self.assertEqual(after_hours_information.get_date(), '2022-04-18')
        self.assertEqual(after_hours_information.get_k_value(), -2.0)
        self.assertEqual(after_hours_information.get_ma20_value(), 81.41)
        self.assertEqual(after_hours_information.get_rsi_value(), 54.0)
        self.assertEqual(after_hours_information.get_foreign_buy(), 137000.0)
        self.assertEqual(after_hours_information.get_investment_trust_buy(), 16000.0)
        self.assertEqual(after_hours_information.get_self_buy(), 10000.0)
        self.assertEqual(after_hours_information.get_news(), '')
        self.assertEqual(after_hours_information.get_monthly_revenue(), 5718985)

        after_hours_information = self.stock.create_stock_after_hours_information(1605)
        self.assertEqual(after_hours_information.get_date(), '2022-04-18')
        self.assertEqual(after_hours_information.get_k_value(), 0.15)
        self.assertEqual(after_hours_information.get_ma20_value(), 30.81)
        self.assertEqual(after_hours_information.get_rsi_value(), 100.0)
        self.assertEqual(after_hours_information.get_foreign_buy(), 29349000.0)
        self.assertEqual(after_hours_information.get_investment_trust_buy(), 2000.0)
        self.assertEqual(after_hours_information.get_self_buy(), 3393544.0)
        self.assertEqual(after_hours_information.get_news(), '係因本公司有價證券於集中交易市場達公布注意交易資訊標準，故公布相關財務業務等重大訊息，以利投資人區別瞭解。')
        self.assertEqual(after_hours_information.get_monthly_revenue(), 28854377)

    def test_get_stock_intraday_information(self):
        stock_intraday_information = self.stock.get_stock_intraday_information()
        self.assertEqual(stock_intraday_information.get_open_price(), 47.3)
        self.assertEqual(stock_intraday_information.get_high_price(), 47.3)
        self.assertEqual(stock_intraday_information.get_low_price(), 46.5)
        self.assertEqual(stock_intraday_information.get_close_price(), 46.5)

    def test_create_stock_intraday_information(self):
        stock_intraday_information = self.stock.create_stock_intraday_information(self.stock.get_stock_id())
        self.assertEqual(stock_intraday_information.get_open_price(), 47.3)
        self.assertEqual(stock_intraday_information.get_high_price(), 47.3)
        self.assertEqual(stock_intraday_information.get_low_price(), 46.5)
        self.assertEqual(stock_intraday_information.get_close_price(), 46.5)

    def test_get_close_price(self):
        close_price = self.stock.get_close_price(1215)
        self.assertEqual(close_price, 81.2)
