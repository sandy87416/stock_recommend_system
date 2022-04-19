from time import sleep
import pandas as pd
import yfinance as yf

stock_id_df = pd.read_csv('stock_id_table.csv')
stock_id_np = stock_id_df['stock_id'].to_numpy()

yahoo_stock_id_np = stock_id_df['yahoo_stock_id'].to_numpy()
public_class_np = stock_id_df['public_class'].to_numpy()

for i in range(len(yahoo_stock_id_np)):
    stock_df = yf.download(str(yahoo_stock_id_np[i]), start='2020-01-01')
    stock_df.reset_index()
    stock_df = stock_df.head(len(stock_df) - 1)
    stock_df.to_csv('data/' + str(stock_id_np[i]) + '.csv')
