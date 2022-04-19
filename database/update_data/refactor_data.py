import pandas as pd

stock_id_df = pd.read_csv('../stock_id_table.csv')
stock_id_np = stock_id_df['stock_id'].to_numpy()


def drop_duplicate_date():
    for stock_id in stock_id_np:
        stock_df = pd.read_csv('../' + str(stock_id) + '.csv')
        stock_df = stock_df.drop_duplicates(subset=['Date'])
        stock_df.to_csv('../' + str(stock_id) + '.csv', index=False)


def buy_astype_int():
    buy_column_list = ['foreign_buy', 'foreign_sell', 'investment_trust_buy', 'investment_trust_sell', 'self_buy',
                       'self_sell']
    for stock_id in stock_id_np:
        print(stock_id)
        company_df = pd.read_csv('../' + str(stock_id) + '.csv')
        for buy_column in buy_column_list:
            company_df[buy_column] = company_df[buy_column].astype('int64')
        company_df.to_csv('../' + str(stock_id) + '.csv', index=False)


drop_duplicate_date()
buy_astype_int()
