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
        recommended_stock_list = self.calculator.read_recommended_stock(2, 0.8)
        # self.assertEqual(recommended_stock_list[0], '8080永利聯合 rsi_6:100.0 win_rate:0.93')
        # self.assertEqual(recommended_stock_list[1], '8477創業家 rsi_6:75.61 win_rate:0.89')
        self.assertEqual(len(recommended_stock_list), 2)

        recommended_stock_list = self.calculator.read_recommended_stock(5, 0.8)
        # self.assertTrue('4712南璋 rsi_6:60.71 win_rate:0.93' in recommended_stock_list)
        # self.assertEqual(recommended_stock_list[1], '9802鈺齊-KY rsi_6:92.0 win_rate:0.93')
        self.assertEqual(len(recommended_stock_list), 22)

        recommended_stock_list = self.calculator.read_recommended_stock(2, 0.7)
        # self.assertEqual(recommended_stock_list[0], '8080永利聯合 rsi_6:100.0 win_rate:0.93')
        # self.assertEqual(recommended_stock_list[1], '8477創業家 rsi_6:75')
        self.assertEqual(len(recommended_stock_list), 6)

    def test_read_stock_odds(self):
        stock_odds_list = self.calculator.read_stock_odds(2330)
        self.assertEqual(stock_odds_list[0], '2330台積電2天賣出勝率:0.69')
        self.assertEqual(stock_odds_list[1], '2330台積電3天賣出勝率:0.6')
        self.assertEqual(len(stock_odds_list), 8)
