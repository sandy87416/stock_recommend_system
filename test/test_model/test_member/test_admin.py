from unittest import TestCase

import pandas as pd

from config import database_path
from model.member.admin import Admin
from model.member.ordinary_member import OrdinaryMember


class TestAdmin(TestCase):
    @classmethod
    def setUpClass(cls):
        member_df = pd.read_csv(database_path + 'member/member.csv')
        password = member_df[member_df['id'] == "t109598092@ntut.org.tw"]['password'].to_numpy()[0]
        cls.admin = Admin("t109598092@ntut.org.tw", password)
        cls.ordinary_member = OrdinaryMember("t109598053@ntut.org.tw", password)

    def test_get_id(self):
        self.assertEqual(self.admin.get_id(), "t109598092@ntut.org.tw")

    def test_get_password(self):
        self.assertEqual(self.admin.get_password(), "islab")

    def test_set_password(self):
        self.assertEqual(self.admin.get_password(), "islab")

        self.admin.set_password("newpassword")

        self.assertEqual(self.admin.get_password(), "newpassword")
        member_df = pd.read_csv(database_path + 'member/member.csv')
        password = member_df[member_df['id'] == self.admin.get_id()]['password'].to_numpy()[0]
        self.assertEqual(password, "newpassword")

        # teardown
        column_index = member_df.columns.get_loc("password")
        row_index = member_df[member_df['id'] == self.admin.get_id()].index
        member_df.iloc[row_index, column_index] = "islab"
        member_df.to_csv(database_path + 'member/member.csv', index=False)

    def test_delete_application_information_data(self):
        self.ordinary_member.apply_premium_member("I want to be the premium member.")
        self.admin.delete_application_information_data(self.ordinary_member.get_id())
        application_information_df = pd.read_csv(database_path + 'member/application_information.csv')
        id_list = application_information_df['id'].to_list()
        content_list = application_information_df['content'].to_list()
        self.assertFalse(self.ordinary_member.get_id() in id_list)
        self.assertFalse("I want to be the premium member." in content_list)

    def test_upgrade_member_level(self):
        member_df = pd.read_csv(database_path + 'member/member.csv')
        id = "t109598053@ntut.org.tw"
        level = member_df[member_df['id'] == id]['level'].to_numpy()[0]
        self.assertEqual(level, 2)
        self.admin.upgrade_member_level(id)

        member_df = pd.read_csv(database_path + 'member/member.csv')
        level = member_df[member_df['id'] == id]['level'].to_numpy()[0]
        self.assertEqual(level, 1)

        application_information_df = pd.read_csv(database_path + 'member/application_information.csv')
        self.assertEqual(len(application_information_df[application_information_df['id'] == id]), 0)

        # teardown
        if level == 1:
            member_df.iloc[member_df[member_df['id'] == id].index, member_df.columns.get_loc("level")] = 2
        member_df.to_csv(database_path + 'member/member.csv', index=False)

    def test_get_application_information_list(self):
        id = 'test@gmail.com'
        password = 'test'
        content = 'apply premium member content'
        ordinary_member = OrdinaryMember(id, password)
        ordinary_member.apply_premium_member(content)
        application_information_list = self.admin.get_application_information_list()
        id_list = [application_information.get_id() for application_information in application_information_list]
        content_list = [application_information.get_content() for application_information in
                        application_information_list]
        self.assertTrue(id in id_list)
        self.assertTrue(content in content_list)
        self.assertEqual(id_list.index(id), content_list.index(content))

        # teardown
        application_information_df = pd.read_csv(database_path + 'member/application_information.csv')
        application_information_df['id'] = application_information_df['id'].astype('str')
        application_information_df = application_information_df.drop(
            application_information_df[application_information_df['id'] == id].index)
        application_information_df.to_csv(database_path + 'member/application_information.csv', index=False)

    def test_logout(self):
        pass  # todo:test
