from unittest import TestCase

from model.stock.intra_day_information import IntraDayInformation


class TestIntraDayInformation(TestCase):
    @classmethod
    def setUpClass(self):
        self.stock = IntraDayInformation('100.00', '95.00', '100.00', '96.00')

    def test_get_end_price(self):
        self.assertEqual(self.stock.get_end_price(), '100.00')

    def test_set_end_price(self):
        self.stock.set_end_price('18.95')
        self.assertEqual(self.stock.get_end_price(), '18.95')

    def test_get_min_price(self):
        self.assertEqual(self.stock.get_min_price(), '95.00')

    def test_set_min_price(self):
        self.stock.set_min_price('237.50')
        self.assertEqual(self.stock.get_min_price(), '237.50')

    def test_get_max_price(self):
        self.assertEqual(self.stock.get_max_price(), '100.00')

    def test_set_max_price(self):
        self.stock.set_max_price('53.90')
        self.assertEqual(self.stock.get_max_price(), '53.90')

    def test_get_start_price(self):
        self.assertEqual(self.stock.get_start_price(), '96.00')

    def test_set_start_price(self):
        self.stock.set_start_price('9.98')
        self.assertEqual(self.stock.get_start_price(), '9.98')
