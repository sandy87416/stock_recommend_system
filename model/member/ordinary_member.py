import pandas as pd

from model.member.application_information import ApplicationInformation
from model.member.member import Member


class OrdinaryMember(Member):
    def create_application_information(self):
        application_information_df = pd.read_csv(
            'D:/stock_recommend_system/database/member/application_information.csv')
        application_information_df = application_information_df.append(pd.DataFrame({
            'account': [self.get_account()],
            'content': [''],
        }))
        application_information_df.to_csv('D:/stock_recommend_system/database/member/application_information.csv',
                                          index=False)
        return ApplicationInformation(self.get_account(), '')

    def apply_premium_member(self, content):
        self.create_application_information()
        application_information_df = pd.read_csv('D:/stock_recommend_system/database/member/application_information.csv')
        row_index = application_information_df[application_information_df['account'] == self.get_account()].index
        column_index = application_information_df.columns.get_loc("content")
        application_information_df.iloc[row_index, column_index] = content
        application_information_df.to_csv('D:/stock_recommend_system/database/member/application_information.csv',
                                          index=False)
        return 'Success'
