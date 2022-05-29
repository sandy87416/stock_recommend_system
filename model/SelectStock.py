class SelectStock:
    __account = ''
    __stock_id = 0

    def __init__(self, account, stock_id):
        self.__account = account
        self.__stock_id = stock_id

    def get_account(self):
        return self.__account

    def get_stock_id(self):
        return self.__stock_id
