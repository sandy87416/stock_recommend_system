from unittest import TestCase

import pandas as pd

from model.member.member import Member
from model.member.ordinary_member import OrdinaryMember


class TestMember(TestCase):
    @classmethod
    def setUpClass(self):
        self.member = OrdinaryMember("t109598087@ntut.org.tw", 'islab1221')

    def test_get_account(self):
        self.assertEqual(self.member.get_account(), 't109598087@ntut.org.tw')

    def test_get_password(self):
        self.assertEqual(self.member.get_password(), 'islab1221')

    def test_set_password(self):
        self.member.set_password('802138')
        self.assertEqual(self.member.get_password(), '802138')

        member_df = pd.read_csv('D:/stock_recommend_system/database/member/member.csv')
        password = member_df[member_df['account'] == "t109598087@ntut.org.tw"]['password'].to_numpy()[0]
        self.assertEqual(password, '802138')

        # teardown
        member_df.iloc[
            member_df[member_df['account'] == self.member.get_account()].index, member_df.columns.get_loc(
                "password")] = "islab1221"
        member_df.to_csv('D:/stock_recommend_system/database/member/member.csv', index=False)

    @classmethod
    def tearDownClass(self) -> None:
        member_df = pd.read_csv('D:/stock_recommend_system/database/member/member.csv')
        member_df = member_df.drop(member_df[member_df['account'] == "t109598087@ntut.org.tw"].index)
        member_df.to_csv('D:/stock_recommend_system/database/member/member.csv', index=False)
