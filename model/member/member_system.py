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

    @staticmethod
    def is_id_and_password_validate(id, password):
        member_df = pd.read_csv(database_path + 'member/member.csv')
        member1_df = member_df[(member_df['id'] == id) & (member_df['password'] == password)]
        level = '-1'
        if len(member1_df) == 1:
            level = str(member_df[member_df['id'] == id]['level'].to_numpy()[0])
        return level
