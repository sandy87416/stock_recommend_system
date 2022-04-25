from unittest import TestCase

from model.member.application_information import ApplicationInformation


class TestApplicationInformation(TestCase):
    @classmethod
    def setUpClass(self):
        self.application_information = ApplicationInformation("t109598053@ntut.org.tw", "administrator")

    def test_get_account(self):
        self.assertEqual(self.application_information.get_account(), "t109598053@ntut.org.tw")

    def test_get_content(self):
        self.assertEqual(self.application_information.get_content(), "administrator")

    def test_set_content(self):
        self.application_information.set_content("I want to be the premium member.")
        self.assertEqual(self.application_information.get_content(), "I want to be the premium member.")
