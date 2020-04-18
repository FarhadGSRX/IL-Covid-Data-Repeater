import bs4
import pandas as pd
import requests
import time

from gspread_pandas import Spread, Client
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
from pathlib import Path

# Paths
script_folder = Path("C:/Users/farha/Google Drive/XS/Git/NicksNewsUpdater/")
backup_folder = Path(script_folder / "backup")
idph_csv_folder = Path(script_folder / "idph_csv")

output_county_file_name = "IDPH Stats County %s.csv"
output_zip_file_name = "IDPH Stats Zip %s.csv"

# All Google Auth and worksheet connection
idph_link = "http://www.dph.illinois.gov/covid19/covid19-statistics"
gsheet_zip_link = "https://docs.google.com/spreadsheets/d/11P36C4z4B2vIXSfgchfAwWfLRnUD0zqg0Ki-MWCiC58/edit#gid=0"
gsheet_county_link = "https://docs.google.com/spreadsheets/d/1sbLLUOqEv_s2eOh3iQyWRw7JOB8rixfu1oBXgPy8zP8/edit#gid=0"
idph_stats_zip_wksht_key = "11P36C4z4B2vIXSfgchfAwWfLRnUD0zqg0Ki-MWCiC58"
idph_stats_county_wksht_key = "1sbLLUOqEv_s2eOh3iQyWRw7JOB8rixfu1oBXgPy8zP8"
creds_path = "C:/Users/farha/Desktop/ExProc-Creds.json"


def the_work():
    # %%
    # Dates
    the_date = datetime.now().strftime("%m-%d")
    the_date_year = datetime.now().strftime("%m-%d-%y")
    the_date_YEAR = datetime.now().strftime("%m-%d-%Y")
    the_date_n_time = datetime.now().strftime("%m-%d-%H%M")
    the_time = datetime.now().strftime("%H:%M")

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_path)
    # If you copy this, make sure the file you are opening is accessible to your service account
    # Ie. Give Sharing/Edit access to ExProc (gdrive-user@exproc.iam.gserviceaccount.com)
    zip_spread = Spread(spread=gsheet_zip_link, creds=credentials)
    county_spread = Spread(spread=gsheet_county_link, creds=credentials)

    # %%
    # Webdriver set up
    # The reason we have to use selenium is because many pages actually load their html within javascript...
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    timeout = 30

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    driver = webdriver.Chrome(chrome_options=options)
    driver.implicitly_wait(300)

    # %%
    # Webdriver Work - First for Zips
    driver.get(idph_link)
    time.sleep(7)

    by_county_button = driver.find_element_by_link_text("By County")
    by_zip_button = driver.find_element_by_link_text("By Zip")

    by_zip_button.click()
    time.sleep(2)
    all_zip_data_button = driver.find_element_by_link_text("All")
    all_zip_data_button.click()
    time.sleep(5)  # Excessive, I know

    zip_soup = bs4.BeautifulSoup(driver.page_source, 'lxml')
    zip_table_soup = zip_soup.find("table", class_="padded-table", id="detailedData")

    by_county_button.click()
    time.sleep(2)
    all_county_data_button = driver.find_element_by_link_text("All")
    all_county_data_button.click()
    time.sleep(5)  # Excessive, I know

    county_soup = bs4.BeautifulSoup(driver.page_source, 'lxml')
    county_table_soup = county_soup.find("table", class_="padded-table", id="detailedData")

    with open(backup_folder / ("backup_soup_zip_%s.txt" % the_date_n_time), "w") as backup_zip_soup:
        backup_zip_soup.writelines(str(zip_soup.encode("utf-8")))
    with open(backup_folder / ("backup_soup_county_%s.txt" % the_date_n_time), "w") as backup_county_soup:
        backup_county_soup.writelines(str(county_soup.encode("utf-8")))

    # %%
    zip_table_headers = zip_table_soup.find_all("th")
    zip_table_headers_arr = [x.get_text() for x in zip_table_headers]
    assert zip_table_headers_arr == ['Zip', 'Positive Cases', 'Deaths']

    county_table_headers = county_table_soup.find_all("th")
    county_table_headers_arr = [x.get_text() for x in county_table_headers]
    assert county_table_headers_arr == ['County', 'Positive Cases', 'Deaths']

    print("Zip first:")
    print(zip_table_soup.find_all("tr")[1:])
    print()
    print("County second:")
    print(county_table_soup.find_all("tr")[1:])

    df_zip_today = pd.DataFrame(columns=zip_table_headers_arr)
    for tr in zip_table_soup.find_all('tr')[1:]:
        tds = tr.find_all('td')
        df_zip_today = df_zip_today.append({'Zip': tds[0].text, 'Positive Cases': tds[1].text, 'Deaths': tds[2].text},
                                           ignore_index=True)

    df_county_today = pd.DataFrame(columns=county_table_headers_arr)
    for tr in county_table_soup.find_all('tr')[1:]:
        tds = tr.find_all('td')
        df_county_today = df_county_today.append(
            {'County': tds[0].text, 'Positive Cases': tds[1].text, 'Deaths': tds[2].text}, ignore_index=True)

    df_zip_today.set_index("Zip", inplace=True)
    df_county_today.set_index("County", inplace=True)

    # %% Assertions Zip - Does the table look as expected?
    assert df_zip_today.index[0] == "60002"  # First zip code in Illinois
    assert int(df_zip_today.index[-1]) >= 62959  # This was the last zip code reported on 4/12/2020
    assert df_zip_today.shape[0] >= 353  # This was the size of the table on 4/12/2020
    assert df_zip_today.Deaths.str.contains(
        "N/A").all()  # The Death column should be "N/A" for all zip codes. If not, we have things to change.

    # %% Assertions County - Does the table look as expected?
    assert df_county_today.index[0] == "Illinois"  # First "county" reported on their table
    assert df_county_today.index[-1] == "Woodford"  # This was the last county code reported on their table on 4/13/2020
    assert df_county_today.shape[0] >= 90  # This was the size of the table on 4/12/2020

    # %% Basic Assertions passed -- Drop and rename things
    # Zip table first
    df_zip_today.drop(columns="Deaths", inplace=True)
    df_zip_today.rename(columns={"Positive Cases": 'Positive_Cases'}, inplace=True)

    # County next
    df_county_today.rename(columns={"Positive Cases": "Positive_Cases"}, inplace=True)

    # %%
    # Open the most recent Zip file for comparison
    zip_changed = False
    df_zip_yday = pd.read_csv(idph_csv_folder / (output_zip_file_name % "latest"), dtype=str)

    # First validate that today's numbers make sense compared to yesterday
    for ix, row in df_zip_yday.iterrows():
        try:
            assert int(df_zip_today.loc[row['Zip'], 'Positive_Cases']) >= int(row.loc["Positive_Cases"]), print(
                int(df_zip_today.loc[row['Zip'], 'Positive_Cases']), "\n", row)
        except AssertionError:
            print("*** Please note, the above Zip Code assertions failed. ***")
            if input("\tContinue? (y/n) ") != "y":
                breakpoint()

    # Now explicitly compare tables to see if they're different
    df_zip_yday.set_index("Zip", inplace=True)
    if df_zip_today.equals(df_zip_yday):
        print("Zip values have not yet changed from latest data.")
    else:
        print("Zip values have been detected as different.")
        # Todo: fix this print(df_zip_today.loc[(df_zip_today != df_zip_yday)])
        zip_changed = True

    # %%
    # Open the most recent County file for comparison
    county_changed = False
    df_county_yday = pd.read_csv(idph_csv_folder / (output_county_file_name % "latest"), dtype=str)

    # First validate that today's numbers make sense compared to yesterday
    for ix, row in df_county_yday.iterrows():
        try:
            assert int(df_county_today.loc[row['County'], 'Positive_Cases']) >= int(row['Positive_Cases']), print(
                int(df_county_today.loc[row['County'], 'Positive_Cases']), "\n", row)
            assert int(df_county_today.loc[row['County'], 'Deaths']) >= int(row['Deaths']), print(
                int(df_county_today.loc[row['County'], 'Deaths']), "\n", row)
        except AssertionError:
            print("*** Please note, the above County Code assertions failed. ***")
            if input("\tContinue? (y/n) ") != "y":
                breakpoint()

    # Now explicitly compare tables to see if they're different
    df_county_yday.set_index("County", inplace=True)
    if df_county_today.equals(df_county_yday):
        print("County values have not yet changed from latest data.")
    else:
        print("County values have been detected as different.")
        # Todo: print(df_county_today.loc[(df_county_today != df_county_yday)])
        county_changed = True

    # %% Now deal with production of Nick's Long version
    if zip_changed:
        df_zip_oldlong = zip_spread.sheet_to_df(index=0, sheet=zip_spread.find_sheet("long"))
        df_zip_today['update_date'] = the_date_YEAR
        df_zip_today['update_time'] = the_time
        df_zip_today.reset_index(inplace=True)
        df_zip_newlong = df_zip_today.append(df_zip_oldlong)[
            ["update_date", "update_time", "Zip", "Positive_Cases"]].reset_index(drop=True)
        df_zip_newlong.to_csv(idph_csv_folder / ("Long Zip %s.csv" % the_date_n_time), index=False)
        zip_spread.df_to_sheet(df_zip_newlong, index=False, sheet="long", start="A1", replace=True)

    if county_changed:
        df_county_oldlong = county_spread.sheet_to_df(index=0, sheet=county_spread.find_sheet("long"))
        df_county_today['update_date'] = the_date_YEAR
        df_county_today['update_time'] = the_time
        df_county_today.reset_index(inplace=True)
        df_county_newlong = df_county_today.append(df_county_oldlong)[
            ["update_date", "update_time", "County", "Positive_Cases", "Deaths"]].reset_index(drop=True)
        df_county_newlong.to_csv(idph_csv_folder / ("Long County %s.csv" % the_date_n_time), index=False)
        county_spread.df_to_sheet(df_county_newlong, index=False, sheet="long", start="A1", replace=True)

    # %% If they were different, let's save them and upload them to sheets
    if zip_changed:
        df_zip_today.to_csv(idph_csv_folder / ("IDPH Stats Zip %s.csv" % the_date_n_time), index=True)
        df_zip_today.to_csv(idph_csv_folder / ("IDPH Stats Zip %s.csv" % "latest"), index=True)
        zip_spread.df_to_sheet(df_zip_today, index=True, sheet=the_date_year, start='A1', replace=True)

    if county_changed:
        df_county_today.to_csv(idph_csv_folder / ("IDPH Stats County %s.csv" % the_date_n_time), index=True)
        df_county_today.to_csv(idph_csv_folder / ("IDPH Stats County %s.csv" % "latest"), index=True)
        county_spread.df_to_sheet(df_county_today, index=True, sheet=the_date_year, start='A1', replace=True)

    # %%
    driver.close()
    print("End of " + the_time + " run.")


if __name__ == "__main__":
    the_work()

    while True:
        if datetime.now().hour < 12:  # Noon
            minutesToSleep = ((11 - datetime.now().hour) * 60) + (59 - datetime.now().minute % 60) + 5
            print("Waiting to run at 12:05pm.")
            time.sleep(minutesToSleep * 60)

        elif datetime.now().hour < 17:  # 5pm
            minutesToSleep = ((16 - datetime.now().hour) * 60) + (59 - datetime.now().minute % 60) + 5
            print("Waiting to run at 5:05pm.")
            time.sleep(minutesToSleep * 60)

        elif datetime.now().hour < 21:  # 9pm
            minutesToSleep = ((20 - datetime.now().hour) * 60) + (59 - datetime.now().minute % 60)
            print("Waiting to run at 9:05pm.")
            time.sleep(minutesToSleep * 60)

        else:
            print("Done for the day.")
            break

        the_work()
