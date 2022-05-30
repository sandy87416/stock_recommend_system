from unittest import TestCase

import pandas as pd

from config import database_path
from model.member.user import User


class TestUser(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User()

    def test_register(self):
        account = 't10598087@ntut.org.tw'
        password = '109598087'
        self.user.register(account, password)
        member_df = pd.read_csv(database_path + 'member/member.csv')
        member1_df = member_df[(member_df['account'] == account) & (member_df['password'] == password)]
        self.assertTrue(len(member1_df) == 1)
        # teardown
        member_df = member_df.drop(
            member_df[(member_df['account'] == account) & (member_df['password'] == password)].index)
        member_df.to_csv(database_path + 'member/member.csv', index=False)

    def test_login(self):
        account = 't10598087@ntut.org.tw'
        password = '109598087'
        self.user.register(account, password)

        login_message = self.user.login(account, password)
        self.assertEqual(login_message, '登入成功')

        member_df = pd.read_csv(database_path + 'member/member.csv')
        member_df = member_df.drop(
            member_df[(member_df['account'] == account) & (member_df['password'] == password)].index)
        member_df.to_csv(database_path + 'member/member.csv', index=False)
        login_message = self.user.login(account, password)
        self.assertEqual(login_message, '登入失敗')