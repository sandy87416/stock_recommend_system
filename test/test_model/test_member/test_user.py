import pandas as pd
from unittest import TestCase
from config import database_path
from model.member.user import User


class TestUser(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User()

    def test_register(self):
        id = 't10598087@ntut.org.tw'
        password = '109598087'
        self.user.register(id, password)
        member_df = pd.read_csv(database_path + 'member/member.csv')
        member1_df = member_df[(member_df['id'] == id) & (member_df['password'] == password)]
        self.assertTrue(len(member1_df) == 1)
        # teardown
        member_df = member_df.drop(
            member_df[(member_df['id'] == id) & (member_df['password'] == password)].index)
        member_df.to_csv(database_path + 'member/member.csv', index=False)
