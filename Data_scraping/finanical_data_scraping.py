#the code scrapes through the Canada's Central Bank webpage, downloads the report with the necessary variables,
#cleans the data (in the periods 2000 - current or 2015 - current) and inserts it to the matching cells in the macropanel file


#load necessary packages
import glob
import os
import pandas as pd
import numpy as np
from openpyxl import load_workbook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


#FUNCTIONS
# this function finds the necessary link by the path and clicks it
def click_button(timeout, path):
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, path)))
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

    button = browser.find_element_by_xpath(path)
    button.click()

# this function finds the necessary link by the path, inserts the value and applies the button
def apply_button(timeout, path, value, apply):
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, path)))
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

    select = Select(browser.find_element_by_xpath(path))
    select.select_by_visible_text(value)

    button = browser.find_element_by_xpath(apply)
    button.click()

#this function opens the last downloaded csv file
def open_downloaded_file():
    directory = "/Users/liudm/Downloads"
    newest_csv = max(glob.iglob(os.path.join(directory, '*.csv')), key=os.path.getctime)
    return newest_csv

#this function inserts the values to the macropanel file and saves them
def insert_data(df.columns, years, df1.columns, sheet):
    for col1, year, col2 in zip(df.columns, years, df1.columns):
        indicator = df[col1].to_frame()
        indicator.reset_index(level=0, inplace=True)
        indicator['index'] = indicator['index'].astype(int)
        row = df1[col2].to_frame()
        row['index'] = indicator['index']
        indicator = indicator[(indicator['index'] >= year)]
        row = row[(row['index'] >= year)]
        indices = np.arange(0, len(indicator))
        for i in range(0, len(indices)):
            ind = indices[i]
            el = row.iloc[i, 0]
            sheet[el] = indicator.iloc(axis=0)[ind, 1]
    workbook.save(filename="macropanel.xlsx")


#SCRAPING: scrape through Canada's bank pages and download nevessary report
option = webdriver.ChromeOptions()
option.add_argument(" - incognito")

browser = webdriver.Chrome(executable_path="/../../../chromedriver", chrome_options=option)

link = "https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1010010801&fbclid=IwAR1Ezp36ZUHzic1u4HiORwVbhNZ15ExXuAXW4do1w9eIFyOKdhog2KkvU4g"
browser.get(link)

click_button(40, "//a[@title='Add/Remove reference period']")
apply_button(40, "//select[@name='transferObject.startYear']", "2000", "//button[@id='cvApplyButton']")
click_button(40, "//a[@id='downloadOverlayLink']")
click_button(40, "//a[@id='downloadAsDisplay']")

#extract necessary variables from downloaded csv to dataframe
df = pd.read_csv(open_downloaded_file(), skiprows=6)
df = df[df['December 2000'].notna()]
variables = ['Assets and liabilities', 'Total assets', 'Total, Government of Canada, direct and guaranteed securities', 'Total, notes in circulation', 'Foreign currency liabilities', 'Canadian dollar deposits, members of Payments Canada 2 6', 'Canadian dollar deposits, Government of Canada', 'Canadian dollar deposits, other 7']
df = df.loc[df['Assets and liabilities'].isin(variables)].reset_index(drop=True)
df = df.rename(columns={'March 2020': 'December 2020'})
assets = df['Assets and liabilities'].to_frame()
df = df.filter(regex=r'(December)')
df.columns = [col.replace('December ', '') for col in df.columns]
df = pd.concat([assets, df], axis=1)
df = df.T
df.columns = df.iloc[0]
df = df.drop(df.index[0])
for col in df.columns:
    df[col] = df[col].str.replace(',','').astype(int)/1000
df['deposits'] = df['Canadian dollar deposits, members of Payments Canada 2 6'] + df['Canadian dollar deposits, Government of Canada'] + df['Canadian dollar deposits, other 7']
df = df.drop(['Canadian dollar deposits, members of Payments Canada 2 6', 'Canadian dollar deposits, Government of Canada', 'Canadian dollar deposits, other 7'], axis = 1)

#prepare variables to insert data to the macropanel file
workbook = load_workbook(filename="macropanel.xlsx")
array = np.arange(134, 155).astype(str)
variables = []
cbassets = ["AV" + el for el in array]
cbgold = ["AW" + el for el in array]
cbfass = ["AX" + el for el in array]
cbgov = ["AY" + el for el in array]
cbnotes = ["AZ" + el for el in array]
cbflia = ["BA" + el for el in array]
cbdep = ["BB" + el for el in array]
df1 = pd.DataFrame(list(zip(cbassets, cbgov, cbnotes, cbflia, cbdep)))
can = workbook["CAN"]
years = [2000, 2015, 2000, 2000, 2015]

# insert the values to the excel file
insert_data(df.columns, years, df1.columns, can)
