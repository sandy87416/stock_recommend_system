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
    def create_selected_stock(id, stock_id):
        return SelectStock(id, stock_id)

    def add_selected_stock(self, id, stock_id):
        selected_stock = self.create_selected_stock(id, stock_id)
        selected_stock_df = pd.read_csv(database_path + 'selected_stock.csv')
        selected_stock_df = pd.concat([selected_stock_df, pd.DataFrame({
            'id': [selected_stock.get_id()],
            'stock_id': [selected_stock.get_stock_id()],
        })])
        selected_stock_df = selected_stock_df.drop_duplicates()
        selected_stock_df.to_csv(database_path + 'selected_stock.csv', index=False)

    def read_selected_stock(self, id):
        selected_stock_df = pd.read_csv(database_path + 'selected_stock.csv')
        selected_stock_df['id'] = selected_stock_df['id'].astype('str')
        selected_stock_df = selected_stock_df.drop_duplicates()
        selected_stock_df = selected_stock_df[selected_stock_df['id'] == id]
        stock_id_np = selected_stock_df['stock_id'].to_numpy()
        selected_stock_list = [self.create_selected_stock(id, stock_id) for stock_id in stock_id_np]
        return selected_stock_list

    @staticmethod
    def delete_selected_stock(id, stock_id):
        selected_stock_df = pd.read_csv(database_path + 'selected_stock.csv')
        selected_stock_df['id'] = selected_stock_df['id'].astype('str')
        selected_stock_df['stock_id'] = selected_stock_df['stock_id'].astype('str')
        selected_stock_df = selected_stock_df.drop(selected_stock_df[(selected_stock_df['id'] == id) & (
                selected_stock_df['stock_id'] == str(stock_id))].index)
        selected_stock_df.to_csv(database_path + 'selected_stock.csv', index=False)

    def get_close_price(self, stock_id):
        stock = self.create_stock(stock_id)
        return stock.get_stock_intraday_information().get_close_price()

    @staticmethod
    def get_stock_classification():
        stock_id_table_df = pd.read_csv(database_path + 'stock_id_table.csv')
        stock_name_np = stock_id_table_df['stock_name'].to_numpy()
        stock_id_np = stock_id_table_df['stock_id'].to_numpy()
        stock_id_table_df['number_name'] = [str(stock_name_np[i]) + ' ' + str(stock_id_np[i]) for i in
                                            range(len(stock_name_np))]
        stock_class_list = list(set(stock_id_table_df['class'].to_list()))
        stock_class_dict = dict()
        for stock_class in stock_class_list:
            stock_class_dict[stock_class] = stock_id_table_df[
                stock_id_table_df['class'] == stock_class]['number_name'].to_list()
        return stock_class_dict

    @staticmethod
    def check_stock_id(stock_id):
        stock_id_table_df = pd.read_csv(database_path + 'stock_id_table.csv')
        stock_np = stock_id_table_df['stock_id'].to_numpy()
        if stock_id in stock_np:
            return True
        return False
