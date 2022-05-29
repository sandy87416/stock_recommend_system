from unittest import TestCase

import pandas as pd

from config import database_path
from model.member.member import Member


class TestMember(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.member = Member("t109598087@ntut.org.tw", 'islab')

    def test_get_account(self):
        self.assertEqual(self.member.get_account(), 't109598087@ntut.org.tw')

    def test_get_password(self):
        self.assertEqual(self.member.get_password(), 'islab')

    def test_set_password(self):
        self.member.set_password('802138')
        self.assertEqual(self.member.get_password(), '802138')

        member_df = pd.read_csv(database_path + 'member/member.csv')
        password = member_df[member_df['account'] == "t109598087@ntut.org.tw"]['password'].to_numpy()[0]
        self.assertEqual(password, '802138')

        # teardown
        member_df.iloc[
            member_df[member_df['account'] == self.member.get_account()].index, member_df.columns.get_loc(
                "password")] = "islab"
        member_df.to_csv(database_path + 'member/member.csv', index=False)

    def test_read_stock_after_hours_information(self):
        stock_after_hours_information = self.member.read_stock_after_hours_information(1605)
        self.assertEqual(stock_after_hours_information.get_date(), '2022-04-18')
        self.assertEqual(stock_after_hours_information.get_k_value(), 0.15)
        self.assertEqual(stock_after_hours_information.get_ma20_value(), 30.81)
        self.assertEqual(stock_after_hours_information.get_rsi_value(), 100.0)
        self.assertEqual(stock_after_hours_information.get_foreign_buy(), 29349000.0)
        self.assertEqual(stock_after_hours_information.get_investment_trust_buy(), 2000.0)
        self.assertEqual(stock_after_hours_information.get_self_buy(), 3393544.0)
        self.assertEqual(stock_after_hours_information.get_news(),
                         '係因本公司有價證券於集中交易市場達公布注意交易資訊標準，故公布相關財務業務等重大訊息，以利投資人區別瞭解。')
        self.assertEqual(stock_after_hours_information.get_monthly_revenue(), 28854377)

    def test_read_stock_intraday_information(self):
        stock_intraday_information = self.member.read_stock_intraday_information(1101)
        self.assertEqual(stock_intraday_information.get_open_price(), 47.3)
        self.assertEqual(stock_intraday_information.get_high_price(), 47.3)
        self.assertEqual(stock_intraday_information.get_low_price(), 46.5)
        self.assertEqual(stock_intraday_information.get_close_price(), 46.5)

    def test_add_selected_stock(self):
        selected_stock_list = self.member.add_selected_stock(2330)
        self.assertEqual(selected_stock_list[0].get_account(), "t109598087@ntut.org.tw")
        self.assertEqual(selected_stock_list[0].get_stock_id(), 2330)

        # teardown
        selected_stock_df = pd.read_csv(database_path + 'selected_stock.csv')
        selected_stock_df = selected_stock_df.drop(selected_stock_df[
                                                       (selected_stock_df['account'] == 't109598087@ntut.org.tw') & (
                                                               selected_stock_df['stock_id'] == 2330)].index)
        selected_stock_df.to_csv(database_path + 'selected_stock.csv', index=False)

    def test_read_selected_stock(self):
        self.member.add_selected_stock(2330)
        selected_stock_list = self.member.read_selected_stock()
        self.assertEqual(selected_stock_list[0].get_account(), "t109598087@ntut.org.tw")
        self.assertEqual(selected_stock_list[0].get_stock_id(), 2330)
        # teardown
        selected_stock_df = pd.read_csv(database_path + 'selected_stock.csv')
        selected_stock_df = selected_stock_df.drop(selected_stock_df[
                                                       (selected_stock_df['account'] == 't109598087@ntut.org.tw') & (
                                                               selected_stock_df['stock_id'] == 2330)].index)
        selected_stock_df.to_csv(database_path + 'selected_stock.csv', index=False)

    def test_delete_selected_stock(self):
        self.member.add_selected_stock(2330)
        selected_stock_list = self.member.read_selected_stock()
        self.assertEqual(selected_stock_list[0].get_account(), "t109598087@ntut.org.tw")
        self.assertEqual(selected_stock_list[0].get_stock_id(), 2330)

        self.member.delete_selected_stock(2330)
        selected_stock_list = self.member.read_selected_stock()
        account_list = [selected_stock.get_account() for selected_stock in selected_stock_list]
        stock_id_list = [selected_stock.get_stock_id() for selected_stock in selected_stock_list]
        self.assertFalse("t109598087@ntut.org.tw" in account_list)
        self.assertFalse(2330 in stock_id_list)

    def test_calculate_current_profit_and_loss(self):
        self.assertEqual(self.member.calculate_current_profit_and_loss(2330, 500, 10, 0.6), 584)
