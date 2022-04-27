class IntraDayInformation:
    __end_price = 0.0
    __min_price = 0.0
    __max_price = 0.0
    __start_price = 0.0

    def __init__(self, end_price, min_price, max_price, start_price):
        self.__end_price = end_price
        self.__min_price = min_price
        self.__max_price = max_price
        self.__start_price = start_price

    def get_end_price(self):
        return self.__end_price

    def set_end_price(self, end_price):
        self.__end_price = end_price

    def get_min_price(self):
        return self.__min_price

    def set_min_price(self, min_price):
        self.__min_price = min_price

    def get_max_price(self):
        return self.__max_price

    def set_max_price(self, max_price):
        self.__max_price = max_price

    def get_start_price(self):
        return self.__start_price

    def set_start_price(self, start_price):
        self.__start_price = start_price
