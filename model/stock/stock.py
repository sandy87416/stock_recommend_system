class Stock:
    __stock_id = 0
    __stock_name = ''
    __stock_company_name = ''
    __stock_classification = ''

    def __init__(self, stock_id, stock_name, stock_company_name, stock_classification):
        self.__stock_id = stock_id
        self.__stock_name = stock_name
        self.__stock_company_name = stock_company_name
        self.__stock_classification = stock_classification

    def get_stock_id(self):
        return self.__stock_id

    def set_stock_id(self, stock_id):
        self.__stock_id = stock_id

    def get_stock_name(self):
        return self.__stock_name

    def set_stock_name(self, stock_name):
        self.__stock_name = stock_name

    # def get_stock_company_name(self):
    #     return self.__stock_company_name
    #
    # def set_stock_company_name(self, stock_company_name):
    #     self.__stock_id = stock_company_name
    #
    # def get_stock_classification(self):
    #     return self.__stock_classification
    #
    # def set_stock_classification(self, stock_classification):
    #     self.__stock_classification = stock_classification
    #
    # def get_stock_after_hours_information(self, stock_id):
    #     pass
    #
    # def get_stock_intraday_information(self, stock_id):
    #     pass
    #
    # def create_stock_intraday_information(self, stock_id):
    #     pass
    #
    # def get_end_price(self, stock_id):
    #     pass

    def get_stock_company_name(self):
        return self.__stock_company_name

    def set_stock_company_name(self, stock_company_name):
        self.__stock_company_name = stock_company_name
