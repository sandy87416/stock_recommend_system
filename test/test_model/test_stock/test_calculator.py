from unittest import TestCase

import numpy as np

np.seterr(invalid='ignore')

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
        self.assertEqual(to_front_end_message_list[1], '8477創業家 rsi_6:75.61 win_rate:0.89')
        self.assertEqual(len(to_front_end_message_list), 1423)

        to_front_end_message_list = self.calculator.read_recommended_stock(5, 0.8)
        self.assertEqual(to_front_end_message_list[0], '4712南璋 rsi_6:60.71 win_rate:0.93')
        self.assertEqual(to_front_end_message_list[1], '9802鈺齊-KY rsi_6:92.0 win_rate:0.93')
        self.assertEqual(len(to_front_end_message_list), 1742)

        to_front_end_message_list = self.calculator.read_recommended_stock(2, 0.7)
        self.assertEqual(to_front_end_message_list[0], '8080永利聯合 rsi_6:100.0 win_rate:0.93')
        self.assertEqual(to_front_end_message_list[1], '8477創業家 rsi_6:75.61 win_rate:0.89')
        self.assertEqual(len(to_front_end_message_list), 1524)
