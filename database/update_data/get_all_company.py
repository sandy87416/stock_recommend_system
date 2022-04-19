import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome('../../chromedriver.exe')
driver.implicitly_wait(3)
driver.get('https://www.google.com.tw/?hl=zh_TW')
driver.maximize_window()
mode_list = [2, 4, 5]

stock_id_list = list()
stock_id_list = list()
company_class_list = list()

for mode in mode_list:
    stock_price_url = 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=' + str(mode)
    driver.get(stock_price_url)

    row_element_list = driver.find_elements(By.XPATH, "//table[@class='h4']//tr//*[text()='ESVUFR']/parent::tr")
    print(len(row_element_list))
    row_split_list = [row_element_list[i].text.split(' ') for i in range(len(row_element_list))]
    stock_id_list += [row_s[0].split()[0] for row_s in row_split_list if row_s[0].split()[0] != '4148']
    stock_id_list += [row_s[0].split()[1] for row_s in row_split_list if row_s[0].split()[0] != '4148']
    company_class_list += [row_split_list[i][4] for i in range(len(row_split_list)) if len(row_split_list[i]) == 6]

df = pd.DataFrame({
    'stock_id': stock_id_list,
    'stock_id': stock_id_list,
    'company_class': company_class_list
}).sort_values('stock_id')

df.to_csv('stock_id_table.csv', index=False)
