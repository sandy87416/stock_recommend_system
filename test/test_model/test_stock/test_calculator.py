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
        recommended_stock1 = {'stock_id': str(8080), 'stock_name': '永利聯合', 'rsi_6': str(100.0), 'odds': str(0.93)}
        recommended_stock2 = {'stock_id': str(8477), 'stock_name': '創業家', 'rsi_6': str(75.61), 'odds': str(0.89)}
        self.assertTrue(recommended_stock1 in recommended_stock_list)
        self.assertTrue(recommended_stock2 in recommended_stock_list)
        self.assertEqual(len(recommended_stock_list), 2)

        recommended_stock_list = self.calculator.read_recommended_stock(5, 0.8)
        recommended_stock1 = {'stock_id': str(4712), 'stock_name': '南璋', 'rsi_6': str(60.71), 'odds': str(0.93)}
        recommended_stock2 = {'stock_id': str(9802), 'stock_name': '鈺齊-KY', 'rsi_6': str(92.0), 'odds': str(0.93)}
        self.assertTrue(recommended_stock1 in recommended_stock_list)
        self.assertTrue(recommended_stock2 in recommended_stock_list)
        self.assertEqual(len(recommended_stock_list), 22)

        recommended_stock_list = self.calculator.read_recommended_stock(2, 0.7)
        recommended_stock1 = {'stock_id': str(8080), 'stock_name': '永利聯合', 'rsi_6': str(100.0), 'odds': str(0.93)}
        recommended_stock2 = {'stock_id': str(8477), 'stock_name': '創業家', 'rsi_6': str(75.61), 'odds': str(0.89)}

        self.assertTrue(recommended_stock1 in recommended_stock_list)
        self.assertTrue(recommended_stock2 in recommended_stock_list)
        self.assertEqual(len(recommended_stock_list), 6)

    def test_read_stock_odds(self):
        stock_odds_list = self.calculator.read_stock_odds(2330)
        stock_odds1 = {'stock_id': str(2330), 'stock_name': '台積電', 'days': str(2), 'odds': str(0.69)}
        stock_odds2 = {'stock_id': str(2330), 'stock_name': '台積電', 'days': str(3), 'odds': str(0.6)}
        self.assertEqual(stock_odds_list[0], stock_odds1)
        self.assertEqual(stock_odds_list[1], stock_odds2)
        self.assertEqual(len(stock_odds_list), 8)
