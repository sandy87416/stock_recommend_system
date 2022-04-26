from unittest import TestCase

import pandas as pd

from model.member.premium_member import PremiumMember


class TestPremiumMember(TestCase):
    @classmethod
    def setUpClass(self):
        self.premium_member = PremiumMember("t109598087@ntut.org.tw", 'islab1221')

    def test_get_account(self):
        self.assertEqual(self.premium_member.get_account(), 't109598087@ntut.org.tw')

    def test_get_password(self):
        self.assertEqual(self.premium_member.get_password(), 'islab1221')

    def test_set_password(self):
        self.premium_member.set_password('802138')
        self.assertEqual(self.premium_member.get_password(), '802138')

        member_df = pd.read_csv('D:/stock_recommend_system/database/member/member.csv')
        password = member_df[member_df['account'] == "t109598087@ntut.org.tw"]['password'].to_numpy()[0]
        self.assertEqual(password, '802138')

        # teardown
        member_df.iloc[
            member_df[member_df['account'] == self.premium_member.get_account()].index, member_df.columns.get_loc(
                "password")] = "islab1221"
        member_df.to_csv('D:/stock_recommend_system/database/member/member.csv', index=False)

    def test_read_recommended_stock(self):
        to_front_end_message_list = self.premium_member.read_recommended_stock(2, 0.8)
        self.assertEqual(to_front_end_message_list[0], '8080永利聯合 rsi_6:100.0 win_rate:0.93')
        self.assertEqual(to_front_end_message_list[1], '3434哲固 rsi_6:95.0 win_rate:0.93')

        to_front_end_message_list = self.premium_member.read_recommended_stock(5, 0.8)
        self.assertEqual(to_front_end_message_list[0], '3712永崴投控 rsi_6:100.0 win_rate:0.92')
        self.assertEqual(to_front_end_message_list[1], '3434哲固 rsi_6:96.61 win_rate:0.91')

    def test_read_stock_odds(self):
        to_front_end_message_list = self.premium_member.read_stock_odds(2330)
        self.assertEqual(to_front_end_message_list[0], '2330台積電2天賣出勝率:0.15')
        self.assertEqual(to_front_end_message_list[1], '2330台積電3天賣出勝率:0.55')

    @classmethod
    def tearDownClass(self) -> None:
        member_df = pd.read_csv('D:/stock_recommend_system/database/member/member.csv')
        member_df = member_df.drop(member_df[member_df['account'] == "t109598087@ntut.org.tw"].index)
        member_df.to_csv('D:/stock_recommend_system/database/member/member.csv', index=False)
