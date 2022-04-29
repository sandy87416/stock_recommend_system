from unittest import TestCase

import pandas as pd

from config import database_path
from model.member.premium_member import PremiumMember


class TestPremiumMember(TestCase):
    @classmethod
    def setUpClass(self):
        self.premium_member = PremiumMember("t109598087@ntut.org.tw", 'islab')

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

    def test_read_stock_odds(self):
        to_front_end_message_list = self.premium_member.read_stock_odds(2330)
        self.assertEqual(to_front_end_message_list[0], '2330台積電2天賣出勝率:0.15')
        self.assertEqual(to_front_end_message_list[1], '2330台積電3天賣出勝率:0.55')
