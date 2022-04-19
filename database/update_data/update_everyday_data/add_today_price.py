import pandas as pd
import yfinance as yf


def update_price(date):
    stock_id_df = pd.read_csv('../data/stock_id_table.csv')
    yahoo_stock_id_np = stock_id_df['yahoo_stock_id'].to_numpy()
    stock_id_np = stock_id_df['stock_id'].to_numpy()

    for i in range(len(yahoo_stock_id_np)):
        stock_df = yf.download(str(yahoo_stock_id_np[i]), start=date)
        stock_df.reset_index()
        stock_df.to_csv('../data/' + str(stock_id_np[i]) + '.csv', mode='a', header=False)
