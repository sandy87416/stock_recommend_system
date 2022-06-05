import pandas as pd
from model import member_system
from config import database_path


class User:
    @staticmethod
    def register(id, password):
        member_df = pd.read_csv(database_path + 'member/member.csv')
        # 判斷帳號重複
        id_np = member_df['id'].to_numpy()
        if id in id_np:
            return '此帳號已經被註冊過'
        result = member_system.create_member(member_df, id, password)
        return result
