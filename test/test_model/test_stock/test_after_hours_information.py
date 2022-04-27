from unittest import TestCase

from model.stock.after_hours_information import AfterHoursInformation


class TestAfterHoursInformation(TestCase):
    @classmethod
    def setUpClass(self):
        self.stock = AfterHoursInformation('2022/04/25', '1.02', '25.35', '66.7', 100, 50, 10, '新聞在這', '23.2')

    def test_get_date(self):
        self.assertEqual(self.stock.get_date(), '2022/04/25')

    def test_set_date(self):
        self.stock.set_date('2022/04/16')
        self.assertEqual(self.stock.get_date(), '2022/04/16')

    def test_get_k_value(self):
        self.assertEqual(self.stock.get_k_value(), '1.02')

    def test_set_k_value(self):
        self.stock.set_k_value('19.58')
        self.assertEqual(self.stock.get_k_value(), '19.58')

    def test_get_ma20_value(self):
        self.assertEqual(self.stock.get_ma20_value(), '25.35')

    def test_set_ma20_value(self):
        self.stock.set_ma20_value('81.23')
        self.assertEqual(self.stock.get_ma20_value(), '81.23')

    def test_get_rsi_value(self):
        self.assertEqual(self.stock.get_rsi_value(), '66.7')

    def test_set_rsi_value(self):
        self.stock.set_rsi_value('21.33')
        self.assertEqual(self.stock.get_rsi_value(), '21.33')

    def test_get_foreign_buy(self):
        self.assertEqual(self.stock.get_foreign_buy(), 100)

    def test_set_foreign_buy(self):
        self.stock.set_foreign_buy(1000)
        self.assertEqual(self.stock.get_foreign_buy(), 1000)

    def test_get_investment_trust_buy(self):
        self.assertEqual(self.stock.get_investment_trust_buy(), 50)

    def test_set_investment_trust_buy(self):
        self.stock.set_investment_trust_buy(520)
        self.assertEqual(self.stock.get_investment_trust_buy(), 520)

    def test_get_self_buy(self):
        self.assertEqual(self.stock.get_self_buy(), 10)

    def test_set_self_buy(self):
        self.stock.set_self_buy(88)
        self.assertEqual(self.stock.get_self_buy(), 88)

    def test_get_news(self):
        self.assertEqual(self.stock.get_news(), '新聞在這')

    def test_set_news(self):
        self.stock.set_news('news hello')
        self.assertEqual(self.stock.get_news(), 'news hello')

    def test_get_monthly_revenue(self):
        self.assertEqual(self.stock.get_monthly_revenue(), '23.2')

    def test_set_monthly_revenue(self):
        self.stock.set_monthly_revenue('0.09')
        self.assertEqual(self.stock.get_monthly_revenue(), '0.09')
