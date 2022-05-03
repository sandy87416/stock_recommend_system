from unittest import TestCase

import numpy as np

from model.stock.calculator import Calculator

np.seterr(invalid='ignore')


class TestCalculator(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.calculator = Calculator()

    def test_calculate_profit_and_loss(self):
        profit_and_loss = self.calculator.calculate_profit_and_loss(600, 605, trading_volume=1000, securities_firm=0.6)
        self.assertEqual(profit_and_loss, 2155)

        profit_and_loss = self.calculator.calculate_profit_and_loss(600, 605, trading_volume=500, securities_firm=0.6)
        self.assertEqual(profit_and_loss, 1077)

        profit_and_loss = self.calculator.calculate_profit_and_loss(600, 605, trading_volume=1000, securities_firm=0.2)
        self.assertEqual(profit_and_loss, 2842)

    def test_read_recommended_stock(self):
        recommended_stock_list = self.calculator.read_recommended_stock(2, 0.8)
        self.assertTrue(
            {'stock_id': 8080, 'stock_name': '永利聯合', 'rsi_6': 100.0, 'odds': 0.93} in recommended_stock_list)
        self.assertTrue({'stock_id': 8477, 'stock_name': '創業家', 'rsi_6': 75.61, 'odds': 0.89} in recommended_stock_list)
        self.assertEqual(len(recommended_stock_list), 2)

        recommended_stock_list = self.calculator.read_recommended_stock(5, 0.8)
        self.assertTrue({'stock_id': 4712, 'stock_name': '南璋', 'rsi_6': 60.71, 'odds': 0.93} in recommended_stock_list)
        self.assertTrue(
            {'stock_id': 9802, 'stock_name': '鈺齊-KY', 'rsi_6': 92.0, 'odds': 0.93} in recommended_stock_list)
        self.assertEqual(len(recommended_stock_list), 22)

        recommended_stock_list = self.calculator.read_recommended_stock(2, 0.7)
        self.assertTrue(
            {'stock_id': 8080, 'stock_name': '永利聯合', 'rsi_6': 100.0, 'odds': 0.93} in recommended_stock_list)
        self.assertTrue(
            {'stock_id': 8477, 'stock_name': '創業家', 'rsi_6': 75.61, 'odds': 0.89} in recommended_stock_list)
        self.assertEqual(len(recommended_stock_list), 6)

    def test_read_stock_odds(self):
        stock_odds_list = self.calculator.read_stock_odds(2330)
        self.assertEqual(stock_odds_list[0], {'stock_id': 2330, 'stock_name': '台積電', 'days': 2, 'odds': 0.69})
        self.assertEqual(stock_odds_list[1], {'stock_id': 2330, 'stock_name': '台積電', 'days': 3, 'odds': 0.6})
        self.assertEqual(len(stock_odds_list), 8)
