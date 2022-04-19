from selenium import webdriver
from selenium.webdriver.common.by import By

import pandas as pd


def update_fa_speaking_meeting_time_csv():
    driver = webdriver.Chrome('../../../chromedriver.exe')

    stock_price_url = 'http://www.money-link.com.tw/stxba/imwcontent0.asp?page=INVC1&ID=INVC1'
    driver.get(stock_price_url)
    driver.implicitly_wait(3)
    driver.maximize_window()

    tr_element_list = driver.find_elements(By.XPATH, '//table[@class="NormalTable"]//tr')
    date_list = list()
    stock_id_list = list()
    time_list = list()
    for tr in tr_element_list:
        row_split = tr.text.split(' ')
        if len(row_split) == 6:
            date_list.append(row_split[0])
            stock_id_list.append(row_split[1])
            time_list.append(row_split[3])

    df = pd.DataFrame({
        'date': date_list,
        'stock_id': stock_id_list,
        'time': time_list,
    })

    df.to_csv('../../fa_speaking_meeting_time.csv', index=False)
    driver.close()


update_fa_speaking_meeting_time_csv()
