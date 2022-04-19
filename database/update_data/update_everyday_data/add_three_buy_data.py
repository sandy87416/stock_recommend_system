# 下載資料套件
import requests as r

# 資料處理套件
import pandas as pd
from datetime import datetime, date
import warnings

warnings.filterwarnings("ignore")


def get_three_buy_df(start_date, end_date):
    three_buy_df = pd.DataFrame()
    date_list = pd.date_range(start_date, end_date, freq='D').strftime("%Y%m%d").tolist()
    for day in date_list:
        try:
            url = 'https://www.twse.com.tw/fund/T86?response=json&date=' + day + '&selectType=ALL'
            res = r.get(url)
            inv_json = res.json()
            df_inv = pd.DataFrame.from_dict(inv_json['data'])
            df_inv.insert(0, '日期', datetime(int(day[:4]), int(day[4:6]), int(day[6:])))
            three_buy_df = three_buy_df.append(df_inv, ignore_index=True)
        except:
            print(day)
    three_buy_df.columns = ['日期', '證券代號', '證券名稱', '外陸資買進股數(不含外資自營商)', '外陸資賣出股數(不含外資自營商)', '外陸資買賣超股數(不含外資自營商)',
                            '外資自營商買進股數', '外資自營商賣出股數', '外資自營商買賣超股數',
                            '投信買進股數', '投信賣出股數', '投信買賣超股數',
                            '自營商買賣超股數', '自營商買進股數(自行買賣)', '自營商賣出股數(自行買賣)',
                            '自營商買賣超股數(自行買賣)', '自營商買進股數(避險)', '自營商賣出股數(避險)', '自營商買賣超股數(避險)',
                            '三大法人買賣超股數']
    three_buy_df.to_csv('three_buy.csv', index=False)


def update_three_buy_data(start_date, end_date):
    stock_id_name_df = pd.read_csv('../data/stock_id_table.csv')
    all_stock_id_np = stock_id_name_df['stock_id'].to_numpy()

    get_three_buy_df(start_date, end_date)
    three_buy_df = pd.read_csv('../update_history_data/three_buy.csv')

    foreign_buy_np = three_buy_df['外陸資買進股數(不含外資自營商)'].to_numpy()
    foreign_sell_np = three_buy_df['外陸資賣出股數(不含外資自營商)'].to_numpy()
    foreign_buy_buy_np = three_buy_df['外資自營商買進股數'].to_numpy()
    foreign_self_buy_np = three_buy_df['外資自營商賣出股數'].to_numpy()

    three_buy_df['外陸資買進股數(不含外資自營商)'] = [int(foreign_buy_np[i].replace(',', '')) for i in range(len(three_buy_df))]
    three_buy_df['外陸資賣出股數(不含外資自營商)'] = [int(foreign_sell_np[i].replace(',', '')) for i in range(len(three_buy_df))]
    three_buy_df['外資自營商買進股數'] = [int(foreign_buy_buy_np[i].replace(',', '')) for i in range(len(three_buy_df))]
    three_buy_df['外資自營商賣出股數'] = [int(foreign_self_buy_np[i].replace(',', '')) for i in range(len(three_buy_df))]

    three_buy_df['foreign_buy'] = three_buy_df['外陸資買進股數(不含外資自營商)'] + three_buy_df['外資自營商買進股數']
    three_buy_df['foreign_sell'] = three_buy_df['外陸資賣出股數(不含外資自營商)'] + three_buy_df['外資自營商賣出股數']

    self_buy_np = three_buy_df['自營商買進股數(自行買賣)'].to_numpy()
    self_sell_np = three_buy_df['自營商賣出股數(自行買賣)'].to_numpy()
    self_buy_buy_np = three_buy_df['自營商買進股數(避險)'].to_numpy()
    self_self_buy_np = three_buy_df['自營商賣出股數(避險)'].to_numpy()

    three_buy_df['自營商買進股數(避險)'] = [str(abc) for abc in three_buy_df['自營商買進股數(避險)']]
    three_buy_df['自營商賣出股數(避險)'] = [str(abc) for abc in three_buy_df['自營商賣出股數(避險)']]

    three_buy_df['自營商買進股數(自行買賣)'] = [int(str(self_buy_np[i]).replace(',', '')) for i in range(len(three_buy_df))]
    three_buy_df['自營商賣出股數(自行買賣)'] = [int(str(self_sell_np[i]).replace(',', '')) for i in range(len(three_buy_df))]
    three_buy_df['自營商買進股數(避險)'] = [int(str(self_buy_buy_np[i]).replace(',', '')) for i in range(len(three_buy_df))]
    three_buy_df['自營商賣出股數(避險)'] = [int(str(self_self_buy_np[i]).replace(',', '').replace('nan', '0')) for i in
                                   range(len(three_buy_df))]

    three_buy_df['self_buy'] = three_buy_df['自營商買進股數(自行買賣)'] + three_buy_df['自營商買進股數(避險)']
    three_buy_df['self_sell'] = three_buy_df['自營商賣出股數(自行買賣)'] + three_buy_df['自營商賣出股數(避險)']

    for stock_id in all_stock_id_np:
        company_df = pd.read_csv('../data/' + str(stock_id) + '.csv')

        date_np = list(set(three_buy_df['日期'].to_list()))
        for date in date_np:
            # print(three_buy_df.dtypes)
            same_company_date_df = three_buy_df[
                (three_buy_df['證券代號'] == str(stock_id)) & (three_buy_df['日期'] == str(date))]

            foreign_buy = int(same_company_date_df['foreign_buy'].to_numpy()[0]) if len(same_company_date_df) > 0 else 0
            foreign_sell = int(same_company_date_df['foreign_sell'].to_numpy()[0]) if len(
                same_company_date_df) > 0 else 0

            investment_trust_buy = int(same_company_date_df['投信買進股數'].to_numpy()[0].replace(',', '')) if len(
                same_company_date_df) > 0 else 0

            investment_trust_sell = int(same_company_date_df['投信賣出股數'].to_numpy()[0].replace(',', '')) if len(
                same_company_date_df) > 0 else 0

            self_buy = int(same_company_date_df['self_buy'].to_numpy()[0]) if len(same_company_date_df) > 0 else 0
            self_sell = int(same_company_date_df['self_sell'].to_numpy()[0]) if len(same_company_date_df) > 0 else 0

            column_index = company_df[company_df['Date'] == date].index

            company_df.iloc[column_index, company_df.columns.get_loc("foreign_buy")] = foreign_buy
            company_df.iloc[column_index, company_df.columns.get_loc("foreign_sell")] = foreign_sell
            company_df.iloc[column_index, company_df.columns.get_loc("investment_trust_buy")] = investment_trust_buy
            company_df.iloc[column_index, company_df.columns.get_loc("investment_trust_sell")] = investment_trust_sell
            company_df.iloc[column_index, company_df.columns.get_loc("self_buy")] = self_buy
            company_df.iloc[column_index, company_df.columns.get_loc("self_sell")] = self_sell

        company_df.to_csv('../data/' + str(stock_id) + '.csv', index=False)



