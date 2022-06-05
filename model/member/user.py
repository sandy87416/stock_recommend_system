import pandas as pd
from model import member_system
from config import database_path


class User:
    @staticmethod
    def register(account, password):
        member_df = pd.read_csv(database_path + 'member/member.csv')
        # 判斷帳號重複
        account_np = member_df['account'].to_numpy()
        if account in account_np:
            return '此帳號已經被註冊過'
        result = member_system.create_member(member_df, account, password)
        return result
