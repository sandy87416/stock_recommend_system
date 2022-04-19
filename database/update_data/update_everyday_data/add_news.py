from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


def update_news_csv():
    driver = webdriver.Chrome('../../../chromedriver.exe')
    # driver.maximize_window()
    driver.minimize_window()
    driver.implicitly_wait(10)

    driver.get('https://mops.twse.com.tw/mops/web/t05st02')

    today_date = str(datetime.now().date())
    today_date_split = today_date.split('-')
    year = str(int(today_date_split[0]) - 1911)
    month = today_date_split[1]
    day = today_date_split[2]

    driver.find_element(By.XPATH, "//*[@id='search_bar1']//*[@name='year']").send_keys(year)
    Select(driver.find_element(By.XPATH, "//*[@id='month']")).select_by_value(month)
    Select(driver.find_element(By.XPATH, "//*[@id='day']")).select_by_value(day)
    driver.find_element(By.XPATH, "//*[contains(@value, ' 查詢 ')]").click()

    tr_list = driver.find_elements(By.XPATH, "//tr[@class='odd' or @class='even']")
    tr_text_split_list = [tr.text.split() for tr in tr_list]

    company_news_list = list()
    for tr_text_split in tr_text_split_list:
        news = ''
        for i in range(4, len(tr_text_split)):
            news += tr_text_split[i]
        company_news_list.append(news)

    news_df = pd.DataFrame({
        'date': [tr_text_split[0] for tr_text_split in tr_text_split_list],
        'time': [tr_text_split[1] for tr_text_split in tr_text_split_list],
        'stock_id': [tr_text_split[2] for tr_text_split in tr_text_split_list],
        'stock_id': [tr_text_split[3] for tr_text_split in tr_text_split_list],
        'company_news': company_news_list,
    })
    news_df.to_csv('../../news.csv', index=False)
    driver.close()


update_news_csv()
