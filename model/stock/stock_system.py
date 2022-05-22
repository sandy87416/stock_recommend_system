import pandas as pd

from config import database_path
from model.stock.stock import Stock


class StockSystem:
    @staticmethod
    def create_stock(stock_id):
        stock_df = pd.read_csv(database_path + 'stock_id_table.csv')
        stock_name = stock_df[stock_df['stock_id'] == stock_id]['stock_name'].to_numpy()[0]
        stock_stock_classification = stock_df[stock_df['stock_id'] == stock_id]['class'].to_numpy()[0]
        return Stock(stock_id, stock_name, stock_name, stock_stock_classification)

    def get_stock_after_hours_information(self, stock_id):
        stock = self.create_stock(stock_id)
        return stock.get_stock_after_hours_information()
