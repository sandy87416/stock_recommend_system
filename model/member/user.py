import pandas as pd
from config import database_path


class User:
    @staticmethod
    def register(account, password):
        member_df = pd.read_csv(database_path + 'member/member.csv')
        member_df = pd.concat([member_df, pd.DataFrame({
            'account': [account],
            'password': [password],
            'level': [2],
        })])
        member_df.to_csv(database_path + 'member/member.csv', index=False)

    @staticmethod
    def login(account, password):
        print(account, password)
        member_df = pd.read_csv(database_path + 'member/member.csv')
        print(member_df)
        member1_df = member_df[(member_df['account'] == account) & (member_df['password'] == password)]
        print(member1_df)
        print(len(member1_df))
        if len(member1_df) == 1:
            return '登入成功'
        else:
            return '登入失敗'
