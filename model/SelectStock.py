class SelectStock:
    __id = ''
    __stock_id = 0

    def __init__(self, id, stock_id):
        self.__id = id
        self.__stock_id = stock_id

    def get_id(self):
        return self.__id

    def get_stock_id(self):
        return self.__stock_id
