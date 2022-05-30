from unittest import TestCase

import pandas as pd

from config import database_path
from model.member.admin import Admin
from model.member.ordinary_member import OrdinaryMember


class TestAdmin(TestCase):
    @classmethod
    def setUpClass(cls):
        member_df = pd.read_csv(database_path + 'member/member.csv')
        password = member_df[member_df['account'] == "t109598092@ntut.org.tw"]['password'].to_numpy()[0]
        cls.admin = Admin("t109598092@ntut.org.tw", password)

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
        column_index = member_df.columns.get_loc("password")
        row_index = member_df[member_df['account'] == self.admin.get_account()].index
        member_df.iloc[row_index, column_index] = "islab"
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

        application_information_df = pd.read_csv(database_path + 'member/application_information.csv')
        self.assertEqual(len(application_information_df[application_information_df['account'] == account]), 0)

        # teardown
        if level == 1:
            member_df.iloc[member_df[member_df['account'] == account].index, member_df.columns.get_loc("level")] = 2
        member_df.to_csv(database_path + 'member/member.csv', index=False)

    def test_get_application_information_zip(self):
        ordinary_member = OrdinaryMember('test', 'test')
        ordinary_member.apply_premium_member('123')
        application_information_zip = self.admin.get_application_information_zip()
        account_list = list()
        content_list = list()
        for account, content in application_information_zip:
            account_list.append(account)
            content_list.append(content)
        self.assertTrue('test' in account_list)
        self.assertTrue('123' in content_list)

        # teardown
        application_information_df = pd.read_csv(database_path + 'member/application_information.csv')
        application_information_df['account'] = application_information_df['account'].astype('str')
        application_information_df = application_information_df.drop(
            application_information_df[application_information_df['account'] == 'test'].index)
        application_information_df.to_csv(database_path + 'member/application_information.csv', index=False)

