import pandas as pd
from config import database_path


class User:
    @staticmethod
    def register(account, password):
        member_df = pd.read_csv(database_path + 'member/member.csv')
        # 判斷帳號重複
        account_np = member_df['account'].to_numpy()
        if account in account_np:
            return '註冊失敗'
        # 寫入member.csv
        member_df = pd.concat([member_df, pd.DataFrame({
            'account': [account],
            'password': [password],
            'level': [2],
        })])
        member_df.to_csv(database_path + 'member/member.csv', index=False)
        return '註冊成功'

    @staticmethod
    def login(account, password):
        level = '-1'
        member_df = pd.read_csv(database_path + 'member/member.csv')
        member1_df = member_df[(member_df['account'] == account) & (member_df['password'] == password)]
        level_np = member1_df['level'].to_numpy()
        if len(level_np) > 0:
            level = level_np[0]
        if len(member1_df) == 1:
            return '登入成功', level
        else:
            return '登入失敗', level
