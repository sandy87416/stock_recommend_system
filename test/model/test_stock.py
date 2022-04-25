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
        pass

    def test_set_stock_classification(self):
        pass

    def test_get_stock_after_hours_information(self):
        pass

    def test_get_stock_intraday_information(self):
        pass

    def test_create_stock_intraday_information(self):
        pass

    def test_get_end_price(self):
        pass
