from model.member.member import Member
from model.stock.calculator import Calculator


class PremiumMember(Member):
    def __init__(self, id, password):
        super().__init__(id, password)
        self.__id = id
        self.__password = password

    @staticmethod
    def read_recommended_stock(days, odds):
        calculator = Calculator()
        recommended_stock_list = calculator.read_recommended_stock(days, odds)
        return recommended_stock_list

    @staticmethod
    def read_stock_odds(stock_id):
        calculator = Calculator()
        stock_odds_list = calculator.read_stock_odds(stock_id)
        return stock_odds_list
