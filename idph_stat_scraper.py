import bs4
import gspread
import pandas as pd
import requests
import time

from gspread_pandas import Spread, Client
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
from pytz import timezone

# The reason we have to use selenium is because many pages actually load their html within javascript...
from selenium import webdriver

timeout = 30

output_county_file_name = "IDPH Stats County %s.csv"
output_zip_file_name = "IDPH Stats Zip %s.csv"

# All Google Auth and worksheet connection
idph_link = "http://www.dph.illinois.gov/covid19/covid19-statistics"
gsheet_zip_link = "https://docs.google.com/spreadsheets/d/11P36C4z4B2vIXSfgchfAwWfLRnUD0zqg0Ki-MWCiC58/edit#gid=0"
gsheet_county_link = "https://docs.google.com/spreadsheets/d/1sbLLUOqEv_s2eOh3iQyWRw7JOB8rixfu1oBXgPy8zP8/edit#gid=0"
gsheet_totals_link = "https://docs.google.com/spreadsheets/d/1MWNebArAjjTTtJdxQcnUakShSbADhccx3xw28L2Nflo/edit#gid=0"
idph_stats_zip_wksht_key = "11P36C4z4B2vIXSfgchfAwWfLRnUD0zqg0Ki-MWCiC58"
idph_stats_county_wksht_key = "1sbLLUOqEv_s2eOh3iQyWRw7JOB8rixfu1oBXgPy8zP8"
idph_stats_totals_wksht_key = "1MWNebArAjjTTtJdxQcnUakShSbADhccx3xw28L2Nflo"


def the_work(creds_path, backup_folder, idph_csv_folder, geo_folder, chrome_options, chrome_path='chromedriver', **kwargs):
    # Dates
    the_date = datetime.now(timezone('US/Central')).strftime("%m-%d")
    the_date_year_yday = datetime.strftime(datetime.now(timezone('US/Central')) - timedelta(1), '%m-%d-%y')
    the_date_year = datetime.now(timezone('US/Central')).strftime("%m-%d-%y")
    the_date_YEAR = datetime.now(timezone('US/Central')).strftime("%m-%d-%Y")
    the_date_n_time = datetime.now(timezone('US/Central')).strftime("%m-%d-%H%M")
    the_time = datetime.now(timezone('US/Central')).strftime("%H:%M")

    print("Starting scraper...{} {}".format(the_date_year, the_time))

    credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_path)
    # If you copy this, make sure the file you are opening is accessible to your service account
    # Ie. Give Sharing/Edit access to ExProc (gdrive-user@exproc.iam.gserviceaccount.com)
    totals_spread, zip_spread, county_spread = None, None, None
    while not (zip_spread and county_spread and totals_spread):
        try:
            if not zip_spread:
                zip_spread = Spread(spread=gsheet_zip_link, creds=credentials)
            if not county_spread:
                county_spread = Spread(spread=gsheet_county_link, creds=credentials)
            if not totals_spread:
                totals_spread = Spread(spread=gsheet_totals_link, creds=credentials)
        except gspread.exceptions.APIError as e:
            print(e)
            print("gspread API Error occurred")
            time.sleep(5)
            continue
        except requests.exceptions.ReadTimeout:
            print("requests ReadTimeout occurred")
            time.sleep(5)
            continue

    driver = webdriver.Chrome(executable_path=chrome_path,
                              options=chrome_options)  # Chrome options are passed into function
    driver.implicitly_wait(300)

    # %%
    # Webdriver Work - First for Zips
    driver.get(idph_link)
    time.sleep(10)

    # Collecting totals
    daily_totals = {"tests_pos": int(driver.find_element_by_id("covid19positive").text.replace(",", "")),
                    "deaths": int(driver.find_element_by_id("covid19deaths").text.replace(",", "")),
                    "total_tests": int(driver.find_element_by_id("covid19totaltest").text.replace(",", ""))#,
                    #"recovered": int(driver.find_element_by_id("covid19recovered").text.replace(",", ""))
                    }

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

    # Todo: Make sure to back this up as well
    with open(backup_folder / ("backup_soup_zip_%s.txt" % the_date_n_time), "w") as backup_zip_soup:
        backup_zip_soup.writelines(str(zip_soup.encode("utf-8")))
    with open(backup_folder / ("backup_soup_county_%s.txt" % the_date_n_time), "w") as backup_county_soup:
        backup_county_soup.writelines(str(county_soup.encode("utf-8")))

    # %%
    zip_table_headers = zip_table_soup.find_all("th")
    zip_table_headers_arr = [x.get_text() for x in zip_table_headers]
    print(zip_table_headers_arr)
    # 9/14/2020 change
    if zip_table_headers_arr[2] == "Confirmed Cases":
        zip_table_headers_arr[2] = "Positive Cases"
    assert zip_table_headers_arr == ['Zip', 'Tested', 'Positive Cases', 'Deaths']

    county_table_headers = county_table_soup.find_all("th")
    county_table_headers_arr = [x.get_text() for x in county_table_headers]
    # 9/14/2020 change
    if county_table_headers_arr[2] == "Confirmed Cases":
        county_table_headers_arr[2] = "Positive Cases"
    assert county_table_headers_arr == ['County', 'Tested', 'Positive Cases', 'Deaths']

    #print("Zip first:")
    #print(zip_table_soup.find_all("tr")[1:])
    #print()
    #print("County second:")
    #print(county_table_soup.find_all("tr")[1:])

    df_zip_today = pd.DataFrame(columns=zip_table_headers_arr)
    for tr in zip_table_soup.find_all('tr')[1:]:
        tds = tr.find_all('td')
        df_zip_today = df_zip_today.append(
            {'Zip': tds[0].text, 'Tested': tds[1].text, 'Positive Cases': tds[2].text, 'Deaths': tds[3].text},
            ignore_index=True)

    df_county_today = pd.DataFrame(columns=county_table_headers_arr)
    for tr in county_table_soup.find_all('tr')[1:]:
        tds = tr.find_all('td')
        df_county_today = df_county_today.append(
            {'County': tds[0].text, 'Tested': tds[1].text, 'Positive Cases': tds[2].text, 'Deaths': tds[3].text},
            ignore_index=True)

    df_zip_today.set_index("Zip", inplace=True)
    df_county_today.set_index("County", inplace=True)

    # %%
    # Totals -- Assertions, Comparisons, and Long form production
    df_totals_oldlong = totals_spread.sheet_to_df(index=0)
    assert daily_totals['tests_pos'] >= int(df_totals_oldlong.iloc[0]['tests_pos'])  # Was the number back on 4/18/2020
    assert daily_totals['deaths'] >= int(df_totals_oldlong.iloc[0]['deaths'])
    assert daily_totals['total_tests'] >= int(df_totals_oldlong.iloc[0]['total_tests'])
    #assert daily_totals['recovered'] >= int(df_totals_oldlong.iloc[0]['recovered'])
    print("Daily Totals Assertions passed.")

    totals_changed = False

    if (daily_totals['tests_pos'] != int(df_totals_oldlong.iloc[0]['tests_pos'])) or \
            (daily_totals['deaths'] != int(df_totals_oldlong.iloc[0]['deaths'])) or \
            (daily_totals['total_tests'] != int(df_totals_oldlong.iloc[0]['total_tests'])): # or \
            #(daily_totals['recovered'] != int(df_totals_oldlong.iloc[0]['recovered'])):
        totals_changed = True
        print("Totals were detected as changed.")

    if totals_changed:
        daily_totals['update_date'] = the_date_YEAR
        daily_totals['update_time'] = the_time
        daily_totals['tests_neg'] = daily_totals['total_tests'] - daily_totals['tests_pos']
        daily_totals['new_tests'] = daily_totals['total_tests'] - int(df_totals_oldlong.iloc[0]['total_tests'])
        df_totals_today = pd.DataFrame(daily_totals, index=[0])

        df_totals_newlong = df_totals_today.append(df_totals_oldlong)[
            ["update_date", "tests_pos", "deaths", "total_tests",
             #"recovered",
             "tests_neg", "new_tests"]].reset_index(
            drop=True)
        df_totals_newlong.to_csv(idph_csv_folder / ("Long Totals %s.csv" % the_date_n_time), index=False)
        totals_spread.df_to_sheet(df_totals_newlong, index=False, sheet="IL_long", start="A1", replace=True)

    # %% Assertions Zip - Does the table look as expected?
    assert df_zip_today.index[0] <= "60002"  # First zip code in Illinois
    assert int(df_zip_today.index[-1]) >= 62959  # This was the last zip code reported on 4/12/2020
    assert df_zip_today.shape[0] >= 353  # This was the size of the table on 4/12/2020
    assert df_zip_today.Deaths.str.contains("N/A").all()  # The Death column should be "N/A" for all zip codes.
    print("Zip Assertions passed.")

    # %% Assertions County - Does the table look as expected?
    assert df_county_today.index[0] == "Illinois"  # First "county" reported on their table
    assert df_county_today.index[-1] == "Woodford"  # This was the last county code reported on their table on 4/13/2020
    assert df_county_today.shape[0] >= 90  # This was the size of the table on 4/12/2020
    print("County Assertions passed.")

    # %% Basic Assertions passed -- Drop and rename things
    # Zip table first
    df_zip_today.drop(columns="Deaths", inplace=True)
    df_zip_today.rename(columns={"Positive Cases": 'Positive_Cases'}, inplace=True)

    # County next
    df_county_today.rename(columns={"Positive Cases": "Positive_Cases"}, inplace=True)

    # %%
    # Open the most recent Zip file for comparison
    zip_changed = False

    # Assume the sheet has already been updated for the day, try grabbing and comparing with that first.
    zip_spread_yday = Spread(spread=gsheet_zip_link, creds=credentials)
    df_zip_yday = zip_spread_yday.sheet_to_df(index=0, sheet=zip_spread.find_sheet(the_date_year))
    if "update_time" in df_zip_yday.columns:  # Oh, so it didn't find it for today, let's grab the one from yesterday
        df_zip_yday = zip_spread_yday.sheet_to_df(index=0, sheet=zip_spread.find_sheet(the_date_year_yday))

    # Now explicitly compare tables to see if they're different
    df_zip_yday.set_index("Zip", inplace=True)
    if df_zip_today.equals(df_zip_yday):
        print("Zip values have not yet changed from latest data.")
    else:
        print("Zip values have been detected as different.")
        zip_changed = True

    # %%
    # Open the most recent County file for comparison
    county_changed = False

    # Assume the sheet has already been updated for the day, try grabbing and comparing with that first.
    county_spread_yday = Spread(spread=gsheet_county_link, creds=credentials)
    df_county_yday = county_spread_yday.sheet_to_df(index=0, sheet=county_spread.find_sheet(the_date_year))
    if "update_time" in df_county_yday.columns:  # Oh, so it didn't find it for today, let's grab the one from yesterday
        df_county_yday = county_spread_yday.sheet_to_df(index=0, sheet=county_spread.find_sheet(the_date_year_yday))

    # Now explicitly compare tables to see if they're different
    df_county_yday.set_index("County", inplace=True)
    if df_county_today.equals(df_county_yday):
        print("County values have not yet changed from latest data.")
    else:
        print("County values have been detected as different.")
        county_changed = True

    # %% If they were different, let's save them and upload them to sheets
    print("\nUploading new sheets if changed.")
    if zip_changed:
        df_zip_today.to_csv(idph_csv_folder / ("IDPH Stats Zip %s.csv" % the_date_n_time), index=True)
        zip_spread.df_to_sheet(df_zip_today, index=True, sheet=the_date_year, start='A1', replace=True)
        print("\tNew Zip was uploaded to Sheets.")
    else:
        print("\tZip version was not uploaded.")

    if county_changed:
        df_county_today.to_csv(idph_csv_folder / ("IDPH Stats County %s.csv" % the_date_n_time), index=True)
        county_spread.df_to_sheet(df_county_today, index=True, sheet=the_date_year, start='A1', replace=True)
        print("\tNew County was uploaded to Sheets.")
    else:
        print("\tCounty version was not uploaded.")

    # %% Now deal with production of Long version
    print("\nProducing Zip and County long versions.")

    # Bring in mapping tools
    census_df = pd.read_csv(geo_folder / "Illinois_Census_200414_1816.csv")
    nofo_map_dict = dict(zip(census_df.CountyName, census_df.NOFO_Region))
    metro_map_dict = dict(zip(census_df.CountyName, census_df.Metro_area))

    if zip_changed:
        df_zip_oldlong = zip_spread.sheet_to_df(index=0, sheet=zip_spread.find_sheet("long"))
        df_zip_today['update_date'] = the_date_YEAR
        df_zip_today['update_time'] = the_time
        df_zip_today.reset_index(inplace=True)
        df_zip_newlong = df_zip_today.append(df_zip_oldlong)[
            ["update_date", "update_time", "Zip", "Positive_Cases", "Tested"]].reset_index(drop=True)
        df_zip_newlong.to_csv(idph_csv_folder / ("Long Zip %s.csv" % the_date_n_time), index=False)
        zip_spread.df_to_sheet(df_zip_newlong, index=False, sheet="long", start="A1", replace=True)
        print("\tZip Long version made and uploaded.")
    else:
        print("\tZip version was not uploaded.")

    if county_changed:
        df_county_oldlong = county_spread.sheet_to_df(index=0, sheet=county_spread.find_sheet("long"))
        df_county_today['update_date'] = the_date_YEAR
        df_county_today['update_time'] = the_time
        # Add NOFO Region
        df_county_today['NOFO_Region'] = df_county_today.index.map(nofo_map_dict)
        df_county_today.loc[df_county_today['NOFO_Region'].isna(), "NOFO_Region"] = df_county_today.index[
            df_county_today['NOFO_Region'].isna()]
        # Add Metro Area
        df_county_today['Metro_Area'] = df_county_today.index.map(metro_map_dict)
        # Chicago and Illinois are not mapped on the Metro mapping file.
        df_county_today.loc[df_county_today.index == "Chicago", "Metro_Area"] = 'Chicago'
        df_county_today.loc[df_county_today.index == "Illinois", "Metro_Area"] = 'Illinois'
        # Leaving unlabeled metro areas as Nulls.

        df_county_today.reset_index(inplace=True)
        df_county_newlong = df_county_today.append(df_county_oldlong)[
            ["update_date", "update_time", "County", "Positive_Cases", "Deaths", "Tested", "NOFO_Region",
             "Metro_Area"]].reset_index(drop=True)
        df_county_newlong.to_csv(idph_csv_folder / ("Long County %s.csv" % the_date_n_time), index=False)
        county_spread.df_to_sheet(df_county_newlong, index=False, sheet="long", start="A1", replace=True)
        print("\tLong editions made and uploaded.")
    else:
        print("\tCounty version was not uploaded.")

    # %% Now producing NOFO Region and Metro Area Rollups directly from County_long and Zip_long directly from gsheets
    if zip_changed or county_changed:
        # cln = county_long_now
        cln = county_spread.sheet_to_df(index=None, sheet=county_spread.find_sheet("long"))
        # I'm not converting the hourly one because as datetimes it includes the wrong day.
        (cln.update_date) = pd.to_datetime(cln.update_date)
        cln.Tested = cln.Tested.apply(lambda x: "0" if x == "" else x)
        cln.Positive_Cases, cln.Deaths, cln.Tested = cln.Positive_Cases.astype(int), cln.Deaths.astype(
            int), cln.Tested.astype(int)

        # County data is ready for roll-up and upload to NOFO_long
        cln_nofo = cln.groupby(by=["update_date", "update_time", "NOFO_Region"]).sum()
        cln_nofo = cln_nofo.sort_index(axis=0, level=[-1, -3], sort_remaining=False)
        totals_spread.df_to_sheet(cln_nofo, index=True, sheet="NOFO_long", start="A1", replace=True)

        # County data is ready for roll-up and upload to Metro_long
        cln_metro = cln.groupby(by=["update_date", "update_time", "Metro_Area"]).sum()
        cln_metro = cln_metro.sort_index(axis=0, level=[-1, -3], sort_remaining=False)
        cln_metro = cln_metro.drop(axis=0, labels="", level=-1)
        totals_spread.df_to_sheet(cln_metro, index=True, sheet="Metro_long", start="A1", replace=True)

    # %%
    driver.close()
    print("End of " + the_time + " run.")

    return zip_changed or county_changed
