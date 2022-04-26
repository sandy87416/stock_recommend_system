class Calculator:

    def __init__(self):
        pass

    @staticmethod
    def calculate_profit_and_loss(buy_price, sell_price, trading_volume=1000, securities_firm=0.6):
        fee = (0.1425 / 100) * securities_firm
        tax = 0.3 / 100
        fee_and_tax = (buy_price * fee + sell_price * tax + sell_price * fee)
        return round((sell_price - buy_price - fee_and_tax) * trading_volume)
