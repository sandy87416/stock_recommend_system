from unittest import TestCase

import pandas as pd

from config import database_path
from model.member.ordinary_member import OrdinaryMember


class TestOrdinaryMember(TestCase):

    @classmethod
    def setUpClass(self):
        self.ordinary_member = OrdinaryMember("t109598087@ntut.org.tw", 'islab1221')

    def test_get_account(self):
        self.assertEqual(self.ordinary_member.get_account(), 't109598087@ntut.org.tw')

    def test_get_password(self):
        self.assertEqual(self.ordinary_member.get_password(), 'islab1221')

    def test_set_password(self):
        self.ordinary_member.set_password('802138')
        self.assertEqual(self.ordinary_member.get_password(), '802138')

        member_df = pd.read_csv(database_path + 'member/member.csv')
        password = member_df[member_df['account'] == "t109598087@ntut.org.tw"]['password'].to_numpy()[0]
        self.assertEqual(password, '802138')

        # teardown
        member_df.iloc[
            member_df[member_df['account'] == self.ordinary_member.get_account()].index, member_df.columns.get_loc(
                "password")] = "islab1221"
        member_df.to_csv(database_path + 'member/member.csv', index=False)

    def test_create_application_information(self):
        application_information = self.ordinary_member.create_application_information()
        self.assertEqual(application_information.get_content(), '')
        application_information_df = pd.read_csv(
            database_path + 'member/application_information.csv')
        account = application_information_df.tail(1)['account'].to_numpy()[0]
        self.assertEqual(account, "t109598087@ntut.org.tw")

        # teardown
        application_information_df = application_information_df.drop(
            application_information_df[
                application_information_df['account'] == self.ordinary_member.get_account()].index)
        application_information_df.to_csv(database_path + 'member/application_information.csv',
                                          index=False)

    def test_apply_premium_member(self):
        apply_result = self.ordinary_member.apply_premium_member("I want to be the premium member.")
        self.assertEqual(apply_result, 'Success')
        application_information_df = pd.read_csv(
            database_path + 'member/application_information.csv')
        content = \
            application_information_df[application_information_df['account'] == self.ordinary_member.get_account()][
                'content'].to_numpy()[0]
        self.assertEqual(content, "I want to be the premium member.")

        # teardown
        application_information_df = application_information_df.drop(application_information_df[
                                                                         application_information_df[
                                                                             'account'] == self.ordinary_member.get_account()].index)
        application_information_df.to_csv(database_path + 'member/application_information.csv',
                                          index=False)

    @classmethod
    def tearDownClass(self) -> None:
        member_df = pd.read_csv(database_path + 'member/member.csv')
        member_df = member_df.drop(member_df[member_df['account'] == "t109598087@ntut.org.tw"].index)
        member_df.to_csv(database_path + 'member/member.csv', index=False)
