import pandas as pd
from config import database_path


class MemberSystem:
    @staticmethod
    def create_member(member_df, id, password):
        # 寫入member.csv
        member_df = pd.concat([member_df, pd.DataFrame({
            'id': [id],
            'password': [password],
            'level': [2],
        })])
        member_df.to_csv(database_path + 'member/member.csv', index=False)
        return '註冊成功'
