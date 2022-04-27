from unittest import TestCase

import pandas as pd

from config import database_path
from model.member.admin import Admin


class TestAdmin(TestCase):
    @classmethod
    def setUpClass(self):
        member_df = pd.read_csv(database_path + 'member/member.csv')
        password = member_df[member_df['account'] == "t109598092@ntut.org.tw"]['password'].to_numpy()[0]
        self.admin = Admin("t109598092@ntut.org.tw", password)

    def test_get_account(self):
        self.assertEqual(self.admin.get_account(), "t109598092@ntut.org.tw")

    def test_get_password(self):
        self.assertEqual(self.admin.get_password(), "islab")

    def test_set_password(self):
        self.assertEqual(self.admin.get_password(), "islab")

        self.admin.set_password("newpassword")

        self.assertEqual(self.admin.get_password(), "newpassword")
        member_df = pd.read_csv(database_path + 'member/member.csv')
        password = member_df[member_df['account'] == self.admin.get_account()]['password'].to_numpy()[0]
        self.assertEqual(password, "newpassword")

        # teardown
        member_df.iloc[member_df[member_df['account'] == self.admin.get_account()].index, member_df.columns.get_loc("password")] = "islab"
        member_df.to_csv(database_path + 'member/member.csv', index=False)

    def test_upgrade_member_level(self):
        member_df = pd.read_csv(database_path + 'member/member.csv')
        account = "t109598053@ntut.org.tw"
        level = member_df[member_df['account'] == account]['level'].to_numpy()[0]
        self.assertEqual(level, 2)
        self.admin.upgrade_member_level(account)

        member_df = pd.read_csv(database_path + 'member/member.csv')
        level = member_df[member_df['account'] == account]['level'].to_numpy()[0]
        self.assertEqual(level, 1)

        # teardown
        if level == 1:
            member_df.iloc[member_df[member_df['account'] == account].index, member_df.columns.get_loc("level")] = 2
        member_df.to_csv(database_path + 'member/member.csv', index=False)
