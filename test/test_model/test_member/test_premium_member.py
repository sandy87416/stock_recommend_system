from unittest import TestCase

import pandas as pd

from config import database_path
from model.member.premium_member import PremiumMember


class TestPremiumMember(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.premium_member = PremiumMember("t109598087@ntut.org.tw", 'islab')

    def test_get_account(self):
        self.assertEqual(self.premium_member.get_account(), 't109598087@ntut.org.tw')

    def test_get_password(self):
        self.assertEqual(self.premium_member.get_password(), 'islab')

    def test_set_password(self):
        self.premium_member.set_password('802138')
        self.assertEqual(self.premium_member.get_password(), '802138')

        member_df = pd.read_csv(database_path + 'member/member.csv')
        password = member_df[member_df['account'] == "t109598087@ntut.org.tw"]['password'].to_numpy()[0]
        self.assertEqual(password, '802138')

        # teardown
        member_df.iloc[
            member_df[member_df['account'] == self.premium_member.get_account()].index, member_df.columns.get_loc(
                "password")] = "islab"
        member_df.to_csv(database_path + 'member/member.csv', index=False)

    def test_read_recommended_stock(self):
        recommended_stock_list = self.premium_member.read_recommended_stock(2, 0.8)
        self.assertTrue('8080永利聯合 rsi_6:100.0 win_rate:0.93' in recommended_stock_list)
        self.assertTrue('8477創業家 rsi_6:75.61 win_rate:0.89' in recommended_stock_list)
        self.assertEqual(len(recommended_stock_list), 2)

        recommended_stock_list = self.premium_member.read_recommended_stock(5, 0.8)
        self.assertTrue('4712南璋 rsi_6:60.71 win_rate:0.93' in recommended_stock_list)
        self.assertTrue('9802鈺齊-KY rsi_6:92.0 win_rate:0.93' in recommended_stock_list)
        self.assertEqual(len(recommended_stock_list), 22)

        recommended_stock_list = self.premium_member.read_recommended_stock(2, 0.7)
        self.assertTrue('8080永利聯合 rsi_6:100.0 win_rate:0.93' in recommended_stock_list)
        self.assertTrue('8477創業家 rsi_6:75.61 win_rate:0.89' in recommended_stock_list)
        self.assertEqual(len(recommended_stock_list), 6)

    def test_read_stock_odds(self):
        stock_odds_list = self.premium_member.read_stock_odds(2330)
        self.assertEqual(stock_odds_list[0], '2330台積電2天賣出勝率:0.69')
        self.assertEqual(stock_odds_list[1], '2330台積電3天賣出勝率:0.6')
        self.assertEqual(len(stock_odds_list), 8)
