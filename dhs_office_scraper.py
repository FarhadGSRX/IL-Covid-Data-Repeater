# %%
import bs4
import pandas as pd
import time

from datetime import datetime, timedelta
from pathlib import Path

# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

timeout = 30

# Paths
script_folder = Path("C:/Users/farha/Google Drive/XS/Git/NicksNewsUpdater/")

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
driver = webdriver.Chrome(chrome_options=options)
driver.implicitly_wait(300)

link = "http://www.dhs.state.il.us/page.aspx?module=12&officetype=&county="
driver.get(link)

# Load up page, make it look how you want
search_button = driver.find_element_by_id("SearchOffice_FindOfficesButton")
search_button.click()

# XPath to find all elements of interest
offices_list = driver.find_elements_by_xpath("//ol[@id='OfficeList']/li")

# List comprehend each office, send to df
df = pd.DataFrame([x.text.split("\n") for x in offices_list],
                  columns=["Name", "Type", "Addr_1", "Addr_2", "Phone", "TTY", "Fax", "Extra_1", "Extra_2", "Extra_3",
                           "Extra_4", "Extra_5", "Extra_6", "Extra_7", "Extra_8"])

# Mild reshaping
df['Closed'] = (df['Name'].str.contains("TEMPORARILY CLOSED") | df['Extra_1'].str.contains("temporarily closed"))
df['City'] = df['Addr_2'].str.extract(r'(.*), IL \d')
df['State'] = 'IL'
df['Zip'] = df['Addr_2'].str.extract(r'IL (\d{5})')
df = df[
    ["Name", "Type", "Closed", "Addr_1", "Addr_2", "City", "State", "Zip", "Phone", "TTY", "Fax", "Extra_1", "Extra_2",
     "Extra_3", "Extra_4", "Extra_5", "Extra_6", "Extra_7", "Extra_8"]]

# Output
df.to_csv("DHS_all_out.csv", index=False)
