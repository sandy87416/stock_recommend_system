class AfterHoursInformation:
    __date = ''
    __k_value = ''
    __ma20_value = 0
    __rsi_value = 0
    __foreign_buy = 0
    __investment_trust_buy = 0
    __self_buy = 0
    __news = ''
    __monthly_revenue = 0

    def __init__(self, date, k_value, ma20_value, rsi_value, foreign_buy, investment_trust_buy, self_buy, news, monthly_revenue):
        self.__date = date
        self.__k_value = k_value
        self.__ma20_value = ma20_value
        self.__rsi_value = rsi_value
        self.__foreign_buy = foreign_buy
        self.__investment_trust_buy = investment_trust_buy
        self.__self_buy = self_buy
        self.__news = news
        self.__monthly_revenue = monthly_revenue

    def get_date(self):
        return self.__date

    def set_date(self, date):
        self.__date = date

    def get_k_value(self):
        return self.__k_value

    def set_k_value(self, k_value):
        self.__k_value = k_value

    def get_ma20_value(self):
        return self.__ma20_value

    def set_ma20_value(self, ma20_value):
        self.__ma20_value = ma20_value

    def get_rsi_value(self):
        return self.__rsi_value

    def set_rsi_value(self, rsi_value):
        self.__rsi_value = rsi_value

    def get_foreign_buy(self):
        return self.__foreign_buy

    def set_foreign_buy(self, foreign_buy):
        self.__foreign_buy = foreign_buy

    def get_investment_trust_buy(self):
        return self.__investment_trust_buy

    def set_investment_trust_buy(self, investment_trust_buy):
        self.__investment_trust_buy = investment_trust_buy

    def get_self_buy(self):
        return self.__self_buy

    def set_self_buy(self, self_buy):
        self.__self_buy = self_buy

    def get_news(self):
        return self.__news

    def set_news(self, news):
        self.__news = news

    def get_monthly_revenue(self):
        return self.__monthly_revenue

    def set_monthly_revenue(self, monthly_revenue):
        self.__monthly_revenue = monthly_revenue





