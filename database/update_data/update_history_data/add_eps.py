from datetime import datetime

import pandas as pd


def update_eps_csv():
    eps_df = pd.read_html('https://www.cnyes.com/twstock/financial4.aspx')[0]
    eps_df['stock_id'] = eps_df['代碼']
    eps_df['eps'] = eps_df['每股EPS(元)']
    eps_df = eps_df[['stock_id', 'eps']]
    eps_df.to_csv('../../eps.csv', index=False)


update_eps_csv()
