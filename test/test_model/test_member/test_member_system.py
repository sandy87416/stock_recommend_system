from unittest import TestCase

import pandas as pd

from config import database_path
from model import MemberSystem


class TestMemberSystem(TestCase):
    def test_create_member(self):
        id = '123456789'
        password = '123456789'
        member_df = pd.read_csv(database_path + 'member/member.csv')
        self.assertEqual(len(member_df[member_df['id'] == id]), 0)

        member_system = MemberSystem()
        self.assertEqual(member_system.create_member(member_df, id, password), '註冊成功')
        member_df = pd.read_csv(database_path + 'member/member.csv')
        id_np = member_df['id'].to_numpy()
        password_np = member_df['password'].to_numpy()
        level_np = member_df['level'].to_numpy()
        index = 0
        for i in range(len(id_np)):
            if id_np[i] == id:
                index = i
        self.assertTrue(id in id_np)
        self.assertEqual(password_np[index], password)
        self.assertEqual(level_np[index], 2)

        # tearDown
        member_df = member_df.drop(member_df[member_df['id'] == id].index)
        member_df.to_csv(database_path + 'member/member.csv', index=False)

    def test_is_id_and_password_validate(self):
        id = '123456789'
        password = '123456789'
        member_df = pd.read_csv(database_path + 'member/member.csv')
        self.assertEqual(len(member_df[member_df['id'] == id]), 0)

        member_system = MemberSystem()
        member_system.create_member(member_df, id, password)
        self.assertEqual(member_system.is_id_and_password_validate(id, password), True)
        self.assertEqual(member_system.is_id_and_password_validate(id, '123'), False)

        # tearDown
        member_df = member_df.drop(member_df[member_df['id'] == id].index)
        member_df.to_csv(database_path + 'member/member.csv', index=False)
