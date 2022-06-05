import pandas as pd
from model import member_system
from config import database_path
from model.member.admin import Admin
from model.member.ordinary_member import OrdinaryMember
from model.member.premium_member import PremiumMember


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

    @staticmethod
    def login(id, password, level):
        if level == '0':
            return Admin(id, password)
        elif level == '1':
            return PremiumMember(id, password)
        elif level == '2':
            return OrdinaryMember(id, password)
        else:
            return None
