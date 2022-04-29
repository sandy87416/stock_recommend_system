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

    def test_read_recommended_stock(self):
        to_front_end_message_list = self.calculator.read_recommended_stock(2, 0.8)
        self.assertEqual(to_front_end_message_list[0], '8080永利聯合 rsi_6:100.0 win_rate:0.93')
        self.assertEqual(to_front_end_message_list[1], '3434哲固 rsi_6:95.0 win_rate:0.93')

        # to_front_end_message_list = self.calculator.read_recommended_stock(5, 0.8)
        # self.assertEqual(to_front_end_message_list[0], '3712永崴投控 rsi_6:100.0 win_rate:0.92')
        # self.assertEqual(to_front_end_message_list[1], '3434哲固 rsi_6:96.61 win_rate:0.91')
