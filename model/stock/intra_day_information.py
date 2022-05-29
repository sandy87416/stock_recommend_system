class IntraDayInformation:
    __open_price = 0.0
    __high_price = 0.0
    __low_price = 0.0
    __close_price = 0.0

    def __init__(self, open_price, high_price, low_price, close_price):
        self.__open_price = open_price
        self.__high_price = high_price
        self.__low_price = low_price
        self.__close_price = close_price

    def get_close_price(self):
        return self.__close_price

    def set_close_price(self, close_price):
        self.__close_price = close_price

    def get_low_price(self):
        return self.__low_price

    def set_low_price(self, low_price):
        self.__low_price = low_price

    def get_high_price(self):
        return self.__high_price

    def set_high_price(self, high_price):
        self.__high_price = high_price

    def get_open_price(self):
        return self.__open_price

    def set_open_price(self, open_price):
        self.__open_price = open_price
