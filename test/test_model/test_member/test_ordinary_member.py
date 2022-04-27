from unittest import TestCase

import pandas as pd

from config import database_path
from model.member.ordinary_member import OrdinaryMember


class TestOrdinaryMember(TestCase):
    def setUp(self):
        self.ordinary_member = OrdinaryMember("t109598087@ntut.org.tw", 'islab')

    def test_get_account(self):
        self.assertEqual(self.ordinary_member.get_account(), 't109598087@ntut.org.tw')

    def test_get_password(self):
        self.assertEqual(self.ordinary_member.get_password(), 'islab')

    def test_set_password(self):
        self.assertEqual(self.ordinary_member.get_password(), 'islab')
        self.ordinary_member.set_password('802138')
        self.assertEqual(self.ordinary_member.get_password(), '802138')

        member_df = pd.read_csv(database_path + 'member/member.csv')
        password = member_df[member_df['account'] == "t109598087@ntut.org.tw"]['password'].to_numpy()[0]
        self.assertEqual(password, '802138')

        # teardown
        member_df.iloc[
            member_df[member_df['account'] == self.ordinary_member.get_account()].index, member_df.columns.get_loc(
                "password")] = "islab"
        member_df.to_csv(database_path + 'member/member.csv', index=False)

    def test_create_application_information(self):
        self.assertEqual(self.ordinary_member.get_application_information(), None)
        self.ordinary_member.create_application_information()

        application_information = self.ordinary_member.get_application_information()
        self.assertNotEqual(application_information, None)
        self.assertEqual(application_information.get_account(), self.ordinary_member.get_account())
        self.assertEqual(application_information.get_content(), '')

    def test_apply_premium_member(self):
        self.ordinary_member.create_application_information()
        apply_result = self.ordinary_member.apply_premium_member("I want to be the premium member.")
        self.assertEqual(apply_result, 'Success')

        application_information = self.ordinary_member.get_application_information()
        self.assertEqual(application_information.get_content(), "I want to be the premium member.")

        apply_df = pd.read_csv(database_path + 'member/application_information.csv')
        content = apply_df[apply_df['account'] == application_information.get_account()]['content'].to_numpy()[0]
        self.assertEqual(content, "I want to be the premium member.")

        # teardown
        apply_df = apply_df.drop(apply_df[apply_df['account'] == self.ordinary_member.get_account()].index)
        apply_df.to_csv(database_path + 'member/application_information.csv', index=False)
