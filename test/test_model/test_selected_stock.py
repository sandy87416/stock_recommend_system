from unittest import TestCase

from model.SelectStock import SelectStock


class TestSelectStock(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.select_stock = SelectStock("t109598087@ntut.org.tw", 2330)

    def test_get_id(self):
        self.assertEqual(self.select_stock.get_id(), 't109598087@ntut.org.tw')

    def test_get_stock_is(self):
        self.assertEqual(self.select_stock.get_stock_id(), 2330)
