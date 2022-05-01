import pandas as pd
from unittest import TestCase

from config import database_path
from model.member.application_information import ApplicationInformation


class TestApplicationInformation(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.account = "t109598053@ntut.org.tw"
        cls.content = "administrator"
        cls.application_information = ApplicationInformation(cls.account, cls.content)

    def test_get_account(self):
        self.assertEqual(self.application_information.get_account(), "t109598053@ntut.org.tw")

    def test_get_content(self):
        self.assertEqual(self.application_information.get_content(), "administrator")

    def test_set_content(self):
        self.assertEqual(self.application_information.get_content(), "administrator")

        self.application_information.set_content("I want to be the premium member.")
        self.assertEqual(self.application_information.get_content(), "I want to be the premium member.")

        application_info_df = pd.read_csv(database_path + 'member/application_information.csv')
        new_content = application_info_df[application_info_df['account'] == self.account]['content'].to_numpy()[0]
        self.assertEqual(new_content, "I want to be the premium member.")

        # teardown
        teardown_index = application_info_df[application_info_df['account'] == self.account].index
        application_info_df.iloc[teardown_index, application_info_df.columns.get_loc("content")] = self.content
        application_info_df.to_csv(database_path + 'member/application_information.csv', index=False)
