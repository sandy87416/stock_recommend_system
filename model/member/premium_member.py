from model.member.member import Member
from model.stock.calculator import Calculator


class PremiumMember(Member):
    def __init__(self, account, password):
        super().__init__(account, password)
        self.__account = account
        self.__password = password

    def read_recommended_stock(self, days, odds):
        calculator = Calculator()
        recommended_stock_list = calculator.read_recommended_stock(days, odds)
        return recommended_stock_list

    def read_stock_odds(self, stock_id):
        calculator = Calculator()
        stock_odds_list = calculator.read_stock_odds(stock_id)
        return stock_odds_list
