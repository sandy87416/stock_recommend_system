from unittest import TestCase

import pandas as pd

from config import database_path
from model.member.premium_member import PremiumMember


class TestPremiumMember(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.premium_member = PremiumMember("t109598087@ntut.org.tw", 'islab')

    def test_get_id(self):
        self.assertEqual(self.premium_member.get_id(), 't109598087@ntut.org.tw')

    def test_get_password(self):
        self.assertEqual(self.premium_member.get_password(), 'islab')

    def test_set_password(self):
        self.premium_member.set_password('802138')
        self.assertEqual(self.premium_member.get_password(), '802138')

        member_df = pd.read_csv(database_path + 'member/member.csv')
        password = member_df[member_df['id'] == "t109598087@ntut.org.tw"]['password'].to_numpy()[0]
        self.assertEqual(password, '802138')

        # teardown
        member_df.iloc[
            member_df[member_df['id'] == self.premium_member.get_id()].index, member_df.columns.get_loc(
                "password")] = "islab"
        member_df.to_csv(database_path + 'member/member.csv', index=False)

    # def test_read_recommended_stock(self):
    #     recommended_stock_list = self.premium_member.read_recommended_stock(2, 0.8)
    #     recommended_stock1 = {'stock_id': str(8080), 'stock_name': '永利聯合', 'rsi_6': str(100.0), 'odds': str(0.93)}
    #     recommended_stock2 = {'stock_id': str(8477), 'stock_name': '創業家', 'rsi_6': str(75.61), 'odds': str(0.89)}
    #     self.assertTrue(recommended_stock1 in recommended_stock_list)
    #     self.assertTrue(recommended_stock2 in recommended_stock_list)
    #     self.assertEqual(len(recommended_stock_list), 2)
    #
    #     recommended_stock_list = self.premium_member.read_recommended_stock(5, 0.8)
    #     recommended_stock1 = {'stock_id': str(4712), 'stock_name': '南璋', 'rsi_6': str(60.71), 'odds': str(0.93)}
    #     recommended_stock2 = {'stock_id': str(9802), 'stock_name': '鈺齊-KY', 'rsi_6': str(92.0), 'odds': str(0.93)}
    #     self.assertTrue(recommended_stock1 in recommended_stock_list)
    #     self.assertTrue(recommended_stock2 in recommended_stock_list)
    #     self.assertEqual(len(recommended_stock_list), 22)
    #
    #     recommended_stock_list = self.premium_member.read_recommended_stock(2, 0.7)
    #     recommended_stock1 = {'stock_id': str(8080), 'stock_name': '永利聯合', 'rsi_6': str(100.0), 'odds': str(0.93)}
    #     recommended_stock2 = {'stock_id': str(8477), 'stock_name': '創業家', 'rsi_6': str(75.61), 'odds': str(0.89)}
    #
    #     self.assertTrue(recommended_stock1 in recommended_stock_list)
    #     self.assertTrue(recommended_stock2 in recommended_stock_list)
    #     self.assertEqual(len(recommended_stock_list), 6)
    #
    # def test_read_stock_odds(self):
    #     stock_odds_list = self.premium_member.read_stock_odds(2330)
    #     stock_odds1 = {'stock_id': str(2330), 'stock_name': '台積電', 'days': str(2), 'odds': str(0.69)}
    #     stock_odds2 = {'stock_id': str(2330), 'stock_name': '台積電', 'days': str(3), 'odds': str(0.6)}
    #     self.assertEqual(stock_odds_list[0], stock_odds1)
    #     self.assertEqual(stock_odds_list[1], stock_odds2)
    #     self.assertEqual(len(stock_odds_list), 8)

    def test_read_stock_after_hours_information(self):
        stock_after_hours_information = self.premium_member.read_stock_after_hours_information(1605)
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
        stock_intraday_information = self.premium_member.read_stock_intraday_information(1101)
        self.assertEqual(stock_intraday_information.get_open_price(), 47.3)
        self.assertEqual(stock_intraday_information.get_high_price(), 47.3)
        self.assertEqual(stock_intraday_information.get_low_price(), 46.5)
        self.assertEqual(stock_intraday_information.get_close_price(), 46.5)

    def test_add_selected_stock(self):
        selected_stock_list = self.premium_member.add_selected_stock(2330)
        self.assertEqual(selected_stock_list[0].get_id(), "t109598087@ntut.org.tw")
        self.assertEqual(selected_stock_list[0].get_stock_id(), 2330)

        # teardown
        selected_stock_df = pd.read_csv(database_path + 'selected_stock.csv')
        selected_stock_df = selected_stock_df.drop(selected_stock_df[
                                                       (selected_stock_df['id'] == 't109598087@ntut.org.tw') & (
                                                               selected_stock_df['stock_id'] == 2330)].index)
        selected_stock_df.to_csv(database_path + 'selected_stock.csv', index=False)

    def test_read_selected_stock(self):
        self.premium_member.add_selected_stock(2330)
        selected_stock_list = self.premium_member.read_selected_stock()
        self.assertEqual(selected_stock_list[0].get_id(), "t109598087@ntut.org.tw")
        self.assertEqual(selected_stock_list[0].get_stock_id(), 2330)
        # teardown
        selected_stock_df = pd.read_csv(database_path + 'selected_stock.csv')
        selected_stock_df = selected_stock_df.drop(selected_stock_df[
                                                       (selected_stock_df['id'] == 't109598087@ntut.org.tw') & (
                                                               selected_stock_df['stock_id'] == 2330)].index)
        selected_stock_df.to_csv(database_path + 'selected_stock.csv', index=False)

    def test_delete_selected_stock(self):
        selected_stock_list = self.premium_member.add_selected_stock(2330)
        self.assertEqual(selected_stock_list[0].get_id(), "t109598087@ntut.org.tw")
        self.assertEqual(selected_stock_list[0].get_stock_id(), 2330)

        selected_stock_list = self.premium_member.delete_selected_stock(2330)
        id_list = [selected_stock.get_id() for selected_stock in selected_stock_list]
        stock_id_list = [selected_stock.get_stock_id() for selected_stock in selected_stock_list]
        self.assertFalse("t109598087@ntut.org.tw" in id_list)
        self.assertFalse(2330 in stock_id_list)

    def test_calculate_current_profit_and_loss(self):
        self.assertEqual(self.premium_member.calculate_current_profit_and_loss(2330, 500, 10, 0.6), 584)

    def test_calculate_profit_and_loss(self):
        profit_and_loss = self.premium_member.calculate_profit_and_loss(600, 605, trading_volume=1000,
                                                                        securities_firm=0.6)
        self.assertEqual(profit_and_loss, 2155)

        profit_and_loss = self.premium_member.calculate_profit_and_loss(600, 605, trading_volume=500,
                                                                        securities_firm=0.6)
        self.assertEqual(profit_and_loss, 1077)

        profit_and_loss = self.premium_member.calculate_profit_and_loss(600, 605, trading_volume=1000,
                                                                        securities_firm=0.2)
        self.assertEqual(profit_and_loss, 2842)

    def test_read_stock_classification(self):
        stock_class_dict = self.premium_member.read_stock_classification()
        self.assertEqual(stock_class_dict['油電燃氣業'][0], '山隆 2616')
