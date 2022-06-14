from unittest import TestCase
from config import database_path
from model.member.application_information import ApplicationInformation
import pandas as pd


class TestApplicationInformation(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.account = "t109598087@ntut.org.tw"
        cls.content = "administrator"
        cls.application_information = ApplicationInformation(cls.account, cls.content)

    @classmethod
    def tearDownClass(cls):
        application_information_df = pd.read_csv(database_path + 'member/application_information.csv')
        application_information_df['id'] = application_information_df['id'].astype('str')
        application_information_df = application_information_df.drop(
            application_information_df[application_information_df['id'] == cls.account].index)
        application_information_df.to_csv(database_path + 'member/application_information.csv', index=False)

    def test_get_id(self):
        self.assertEqual(self.application_information.get_id(), "t109598087@ntut.org.tw")

    def test_get_content(self):
        self.assertEqual(self.application_information.get_content(), "administrator")

    def test_set_content(self):
        self.assertEqual(self.application_information.get_content(), "administrator")

        self.application_information.set_content("I want to be the premium member.")
        self.assertEqual(self.application_information.get_content(), "I want to be the premium member.")

    def test_create_content_to_database(self):
        id = self.application_information.get_id()
        content = self.application_information.get_content()
        application_information = ApplicationInformation(id, content)
        application_information_df = pd.read_csv(database_path + 'member/application_information.csv')
        self.assertEqual(len(application_information_df[application_information_df['id'] == id]), 0)

        application_information.create_content_to_database()
        application_information_df = pd.read_csv(database_path + 'member/application_information.csv')
        self.assertEqual(len(application_information_df[application_information_df['id'] == id]), 1)
        self.assertEqual(len(application_information_df[application_information_df['content'] == content]), 1)

