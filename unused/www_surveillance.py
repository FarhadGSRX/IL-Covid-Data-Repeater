# %%
import requests
import bs4
import hashlib
import json
import re
import time

from gspread_pandas import Spread, Client
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path

# The reason we have to use selenium is because many pages actually load their html within javascript...
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

timeout = 30

# Local Variables
script_folder = Path("C:/Users/farha/Google Drive/XS/Git/NicksNewsUpdater/")
arbitrary_wait_time = 4

# Web access relevant variables
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/farha/Desktop/ExProc-Creds.json", scope)
hyperlink_format = '=HYPERLINK("{url}","{text} - {time}")'  # hyperlink_format.format(url="google.com", text="Ello", time="14:14")

# Set up gspread access
client = Spread(spread="https://docs.google.com/spreadsheets/d/1fWt1l6g815OUAj_8dA9DODd6PO3N2_g0Y_glkY6inpQ/",
                creds=credentials)
state_sheet = client.find_sheet("States_Gov")
county_sheet = client.find_sheet("IL_Counties_DPH")
city_sheet = client.find_sheet("Cities")
data_sheet = client.find_sheet("updater_data")

assert state_sheet
assert county_sheet
assert data_sheet

# Download sheets first
df_state_last = client.sheet_to_df(header_rows=2, start_row=3, sheet=state_sheet)
df_county_last = client.sheet_to_df(header_rows=1, start_row=1, formula_columns=[4, 5], sheet=county_sheet)

# Download data sheet
df_data_sheet = client.sheet_to_df(header_rows=1, start_row=1, sheet=data_sheet)


def split_hyperlink_formula(formula):
    return re.findall('=HYPERLINK\("(.*)","(.*) - (.*)"\)', formula)[0]


def get_link_and_tgt(driver, link, tag_type, search_tag):
    driver.get(link)

    if tag_type == "xpath":
        try:
            WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(By.XPATH, search_tag))
        except TimeoutException:
            driver.quit()
        elem = driver.find_element(By.XPATH, search_tag)
        elem_text = elem.text

    return elem_text


# Start us up
driver = webdriver.Chrome()  # IF it's not in local folder: webdriver.Chrome(executable_path='chromedriver')
driver.implicitly_wait(arbitrary_wait_time)

for ix, row in df_county_last.iterrows():
    for col in ["Press Releases", "Twitter"]:
        if row[col]:
            link, last_time, last_text = split_hyperlink_formula(row[col])
            search_tag = df_data_sheet.loc[link]['Xpath']

            elem_text = get_link_and_tgt(driver, link, "xpath", search_tag)

            if elem_text != re.findall('=HYPERLINK\("(.*)","', row[col])[0]:

driver.quit()
# %%

# The process this time around:
# Create dataframe of links, their cell coords, current cell contents

# Create multithread processor...

# Assign links to threader

# For each link...
# Detect if updated first...
# Then detect if that update is interesting for us
# If so... send a response back through thread which then updates the original dataframe with the relevant info

# Once all links are checked, we can respool the dataframe and look for the ones we need to update.
# Batch updates somehow?


# Worksheet relevant variables:
# [<Worksheet 'Main Sheet' id:0>, <Worksheet 'updater_data' id:2044837808>]
first_link_row = 3
main_pc_col = 5
fbyt_pc_col = 6

# Go get list of links to read through
main_pc_gov_list = main_sheet.col_values(main_pc_col, value_render_option="FORMULA")[first_link_row - 1:-1]  # end on -1
main_pc_fbyt_list = main_sheet.col_values(fbyt_pc_col, value_render_option="FORMULA")[
                    first_link_row - 1:-1]  # end on -1

tag_dict = {}
tag_link_list = data_sheet.col_values(1, value_render_option="FORMULA")[1:]
tag_tag_list = data_sheet.col_values(2, value_render_option="FORMULA")[1:]
tag_dict = {tag_link_list[i]: (tag_tag_list[i] if i < len(tag_tag_list) else "") for i in range(len(tag_link_list))}

# Now strip the link_list to just the hyperlinks
pattern = re.compile("=HYPERLINK\(\"(.*)\",\"")
main_pc_gov_list_clean = [re.search(pattern, value).group(1) if "HYPERLINK" in value else value for value in
                          main_pc_gov_list]
main_pc_fbyt_list_clean = [re.search(pattern, value).group(1) if "HYPERLINK" in value else value for value in
                           main_pc_fbyt_list]

# Tell everyone that we're updating so they don't change anything:
main_sheet.update_cell(1, 1, "Updating!")
update_time = datetime.now().strftime("%m/%d %H:%M")


# %%
def insert_a_column(sheet_id,
                    col_index):  # This is the gspread index of where the new column and data go on the updater_sheet (origin 1,1)
    insert_col_request = []
    insert_col_request.append({"insertDimension": {
        "range": {"sheetId": sheet_id, "dimension": "COLUMNS", "startIndex": col_index - 1, "endIndex": col_index},
        "inheritFromBefore": True}})
    body = {'requests': insert_col_request}
    wksheet.batch_update(body)
    data_sheet.update_cell(1, col_index, update_time)


def get_main_content(soup, nav=""):
    try:
        if "class" in nav and "id" in nav:
            nav = nav.split(maxsplit=5)
        elif "class" in nav or "id" in nav:
            nav = nav.split(maxsplit=3)
        elif "string" in nav or "tag" in nav:
            nav = nav.split(maxsplit=1)
        nav = {nav[ix]: nav[ix + 1] for ix in range(len(nav))[::2]}
    except FileNotFoundError:
        nav = {}

    print("\t", nav)

    if "string" in nav.keys():
        result = ",".join([str(x) for x in soup.find_all(string=re.compile(nav["string"]))])

    elif "tag" in nav.keys():
        if "class" in nav.keys():
            if "id" in nav.keys():  # tag, class, and id
                result = ",".join([x.get_text() for x in soup.find_all(nav["tag"], class_=nav["class"], id=nav["id"])])
            else:  # tag and class only
                result = ",".join([x.get_text() for x in soup.find_all(nav["tag"], class_=nav["class"])])
        elif "id" in nav.keys():  # tag and id only
            result = ",".join([x.get_text() for x in soup.find_all(nav["tag"], id=nav["id"])])
        else:  # tag only
            result = ",".join([x.get_text() for x in soup.find_all(nav["tag"])])

    else:  # nothing in nav
        assert nav == {}
        result = ",".join([x.get_text() for x in soup.find_all("body")])

    return result


def get_link_hash_and_nav(link, last_nav, last_hash,
                          driver):  # This function manages the updating and reading of the data bg sheet
    print("\t", last_nav, last_hash)
    driver.get(link)
    time.sleep(arbitrary_wait_time)
    soup = bs4.BeautifulSoup(driver.page_source, 'lxml')

    try:  # Was already on data background sheet
        current_row_index = tag_link_list.index(link)
        new_nav = tag_dict[link]
        print(new_nav)
        print(last_nav)
        nav_changed = last_nav != new_nav

        if nav_changed:  # Was already on sheet and nav has changed
            data_sheet.update_cell(current_row_index + 2, 1, link)
            data_sheet.update_cell(current_row_index + 2, 3, '=HYPERLINK("' + link + '","New Nav")')

            content = get_main_content(soup, new_nav)
            new_hash = hashlib.sha224(content.encode("utf-8")).hexdigest()


        else:  # Nav has not changed so let's actually compare hashes
            content = get_main_content(soup, new_nav)
            new_hash = hashlib.sha224(content.encode("utf-8")).hexdigest()

            if new_hash != last_hash:  # So hash has changed
                data_sheet.update_cell(current_row_index + 2, 1, link)
                data_sheet.update_cell(current_row_index + 2, 3, '=HYPERLINK("' + link + '","Updated")')


    except ValueError:  # Implies that this link was not in the databackground sheet yet
        new_nav = "tag body"
        # Write new link at bottom
        curr_row = len(data_sheet.col_values(1, value_render_option="FORMULA")) + 1
        data_sheet.update_cell(curr_row, 1, link)
        data_sheet.update_cell(curr_row, 3, '=HYPERLINK("' + link + '","First Check")')

        content = get_main_content(soup, new_nav)
        new_hash = hashlib.sha224(content.encode("utf-8")).hexdigest()

    print("\t\t", new_hash)
    return new_hash, new_nav


def update_one_link(link, driver=-1, ix=-1, col_index=-1):  # This method manages the main_sheet changes
    print(link)
    seen_before = link in webhx.keys()
    print("seen ", seen_before)
    if seen_before:
        last_nav = webhx[link]["last_nav"]
        if last_nav == "tag body":
            last_nav = ""
        last_hash = webhx[link]["hash"]
    else:
        last_nav = ""
        last_hash = ""

    print("next", last_nav, last_hash)

    if driver == -1:
        driver = webdriver.Chrome()
        driver.implicitly_wait(arbitrary_wait_time)
        new_hash, new_nav = get_link_hash_and_nav(link, last_nav, last_hash, driver)
        driver.close()
    else:
        new_hash, new_nav = get_link_hash_and_nav(link, last_nav, last_hash, driver)

    print("new ones", new_nav, new_hash)

    if seen_before:  # Link has been seen before
        same_hash = webhx[link]['hash'] == new_hash
        same_nav = new_nav == last_nav

        if not same_hash:  # Website has changed
            webhx[link]['hash'] = new_hash
            if ix != -1 and col_index != -1:
                main_sheet.update_cell(first_link_row + ix, col_index,
                                       '=HYPERLINK("' + link + '","' + update_time + '")')

            if not same_nav:  # Changed hash and new nav
                webhx[link]['last_nav'] = new_nav

    else:  # Link has not been seen before
        webhx[link] = {'hash': new_hash, 'last_nav': new_nav}
        if ix != -1 and col_index != -1:
            main_sheet.update_cell(first_link_row + ix, col_index, '=HYPERLINK("' + link + '","' + update_time + '")')

    if ix == -1 and col_index == -1:
        with open(webjson_path, "w") as data_once:
            json.dump(webhx, data_once)


def read_and_update_col(column_link_list, col_index,
                        driver):  # Input column is one of the cleaned link lists, origin (1,1)
    for ix, link in enumerate(column_link_list):
        if link == "":  # If link was empty, otherwise it crashes lol
            continue
        update_one_link(link, driver, ix, col_index)


def debug(link):
    driver = webdriver.Chrome()
    driver.implicitly_wait(arbitrary_wait_time)

    driver.get(link)
    time.sleep(arbitrary_wait_time)
    soup = bs4.BeautifulSoup(driver.page_source, 'lxml')
    driver.close()
    return soup


if __name__ == "__main__":
    while True:
        minutesToSleep = 60 - datetime.now().minute % 60
        time.sleep(minutesToSleep * 60)

        driver = webdriver.Chrome()
        driver.implicitly_wait(arbitrary_wait_time)

        # do business here
        insert_a_column(2044837808, 3)
        read_and_update_col(main_pc_gov_list_clean, main_pc_col, driver)
        read_and_update_col(main_pc_fbyt_list_clean, fbyt_pc_col, driver)

        # close business here
        driver.quit()
        main_sheet.update_cell(1, 1, "State")
        with open(webjson_path, "w") as data:
            json.dump(webhx, data)
        print(update_time, " - Done")
