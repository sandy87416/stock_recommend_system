from model.stock.calculator import Calculator


class MemberController:
    def __init__(self):
        pass

    def create_calculator(self):
        return Calculator()

    def read_recommend_stock(self, days, odds):
        calculator = self.create_calculator()
        recommended_stock_list = calculator.read_recommended_stock(days, odds)
        return recommended_stock_list
