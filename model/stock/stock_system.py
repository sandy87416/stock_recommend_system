import pandas as pd

from config import database_path
from model.SelectStock import SelectStock
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

    def get_stock_intraday_information(self, stock_id):
        stock = self.create_stock(stock_id)
        return stock.get_stock_intraday_information()

    @staticmethod
    def create_selected_stock(account, stock_id):
        return SelectStock(account, stock_id)

    def add_selected_stock(self, account, stock_id):
        selected_stock = self.create_selected_stock(account, stock_id)
        selected_stock_df = pd.read_csv(database_path + 'selected_stock.csv')
        selected_stock_df = pd.concat([selected_stock_df, pd.DataFrame({
            'account': [selected_stock.get_account()],
            'stock_id': [selected_stock.get_stock_id()],
        })])
        selected_stock_df.to_csv(database_path + 'selected_stock.csv', index=False)

        # return selected_stock_list
        selected_stock_df = selected_stock_df[selected_stock_df['account'] == account]
        stock_id_np = selected_stock_df['stock_id'].to_numpy()
        selected_stock_list = [self.create_selected_stock(account, stock_id) for stock_id in stock_id_np]
        return selected_stock_list
