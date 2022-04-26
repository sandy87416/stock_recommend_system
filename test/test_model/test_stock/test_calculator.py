from unittest import TestCase

from model.stock.stock import Stock
from model.stock.calculator import Calculator


class TestCalculator(TestCase):
    @classmethod
    def setUpClass(self):
        self.calculator = Calculator()

    def test_calculate_profit_and_loss(self):
        profit_and_loss = self.calculator.calculate_profit_and_loss(600, 605, trading_volume=1000, securities_firm=0.6)
        self.assertEqual(profit_and_loss, 2155)

        profit_and_loss = self.calculator.calculate_profit_and_loss(600, 605, trading_volume=500, securities_firm=0.6)
        self.assertEqual(profit_and_loss, 1077)

        profit_and_loss = self.calculator.calculate_profit_and_loss(600, 605, trading_volume=1000, securities_firm=0.2)
        self.assertEqual(profit_and_loss, 2842)
