from unittest import TestCase

from model.stock.intraday_information import IntraDayInformation


class TestIntraDayInformation(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stock = IntraDayInformation('100.00', '95.00', '100.00', '96.00')

    def test_get_open_price(self):
        self.assertEqual(self.stock.get_open_price(), '100.00')

    def test_set_open_price(self):
        self.stock.set_open_price('18.95')
        self.assertEqual(self.stock.get_open_price(), '18.95')

    def test_get_high_price(self):
        self.assertEqual(self.stock.get_high_price(), '95.00')

    def test_set_high_price(self):
        self.stock.set_high_price('237.50')
        self.assertEqual(self.stock.get_high_price(), '237.50')

    def test_get_low_price(self):
        self.assertEqual(self.stock.get_low_price(), '100.00')

    def test_set_low_price(self):
        self.stock.set_low_price('53.90')
        self.assertEqual(self.stock.get_low_price(), '53.90')

    def test_get_close_price(self):
        self.assertEqual(self.stock.get_close_price(), '96.00')

    def test_set_close_price(self):
        self.stock.set_close_price('9.98')
        self.assertEqual(self.stock.get_close_price(), '9.98')
