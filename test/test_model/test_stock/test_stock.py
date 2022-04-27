from unittest import TestCase

from model.stock.stock import Stock


class TestStock(TestCase):
    @classmethod
    def setUpClass(self):
        self.stock = Stock(1101, '台泥', '台灣水泥', '水泥工業')

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

    def test_get_stock_after_hours_information(self):
        date, k_value, ma20_value, rsi_value, foreign_buy, investment_trust_buy, self_buy, news, monthly_revenue = \
            self.stock.get_stock_after_hours_information(1215)
        self.assertEqual(date, '2022-04-18')
        self.assertEqual(k_value, '')
        self.assertEqual(ma20_value, 0)
        self.assertEqual(rsi_value, 100.0)
        self.assertEqual(foreign_buy, '0')
        self.assertEqual(investment_trust_buy, '0')
        self.assertEqual(self_buy, '0')
        self.assertEqual(news, '')
        self.assertEqual(monthly_revenue, 5718985)

    def test_get_stock_intraday_information(self):
        end_price, min_price, max_price, start_price = self.stock.get_stock_intraday_information(1215)
        self.assertEqual(end_price, 81.2)
        self.assertEqual(min_price, 81.1)
        self.assertEqual(max_price, 83.3)
        self.assertEqual(start_price, 83.3)

    def test_create_stock_intraday_information(self):
        stock_intraday_information = self.stock.create_stock_intraday_information(self.stock.get_stock_id())
        self.assertEqual(stock_intraday_information.get_end_price(), 46.5)
        self.assertEqual(stock_intraday_information.get_min_price(), 46.5)
        self.assertEqual(stock_intraday_information.get_max_price(), 47.3)
        self.assertEqual(stock_intraday_information.get_start_price(), 47.3)

    def test_get_end_price(self):
        end_price = self.stock.get_end_price(1215)
        self.assertEqual(end_price, 81.2)
