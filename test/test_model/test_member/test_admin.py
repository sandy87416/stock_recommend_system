from unittest import TestCase

from model.member.admin import Admin


class TestAdmin(TestCase):
    @classmethod
    def setUpClass(self):
        self.admin = Admin("t109598053@ntut.org.tw", "islab")

    def test_get_account(self):
        self.assertEqual(self.admin.get_account(), "t109598053@ntut.org.tw")

    def test_get_password(self):
        self.assertEqual(self.admin.get_password(), "islab")

    def test_set_password(self):
        self.admin.set_password("newpassword")
        self.assertEqual(self.admin.get_password(), "newpassword")

    def test_upgrade_member_level(self, account):
        pd.re
        # 存入資料庫?
