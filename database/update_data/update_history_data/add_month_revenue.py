from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


def update_month_revenue_csv():
    driver = webdriver.Chrome('../../../chromedriver.exe')
    # driver.maximize_window()
    driver.minimize_window()
    driver.implicitly_wait(10)

    driver.get('https://stock.wespai.com/income')

    tr_list = driver.find_elements(By.XPATH, '//tr')

    tr_text_split_list = [tr.text.split() for tr in tr_list if len(tr.text.split()) > 0 and
                          tr.text.split()[0].isnumeric() and len(tr.text.split()[0]) == 4]

    month_revenue_df = pd.DataFrame({
        'stock_id': [tr_text_split[0] for tr_text_split in tr_text_split_list],
        'month_revenue': [tr_text_split[7] for tr_text_split in tr_text_split_list],
    })

    month_revenue_df.to_csv('../../month_revenue.csv', index=False)


update_month_revenue_csv()
