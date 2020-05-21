# This script assumes that there is an update to report.
import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 10)

from gspread_pandas import Spread, Client
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
from pytz import timezone



# All Google Auth and worksheet connection
idph_link = "http://www.dph.illinois.gov/covid19/covid19-statistics"

gsheet_zip_link = "https://docs.google.com/spreadsheets/d/11P36C4z4B2vIXSfgchfAwWfLRnUD0zqg0Ki-MWCiC58/edit#gid=0"
gsheet_county_link = "https://docs.google.com/spreadsheets/d/1sbLLUOqEv_s2eOh3iQyWRw7JOB8rixfu1oBXgPy8zP8/edit#gid=0"
gsheet_totals_link = "https://docs.google.com/spreadsheets/d/1MWNebArAjjTTtJdxQcnUakShSbADhccx3xw28L2Nflo/edit#gid=0"
idph_stats_zip_wksht_key = "11P36C4z4B2vIXSfgchfAwWfLRnUD0zqg0Ki-MWCiC58"
idph_stats_county_wksht_key = "1sbLLUOqEv_s2eOh3iQyWRw7JOB8rixfu1oBXgPy8zP8"
idph_stats_totals_wksht_key = "1MWNebArAjjTTtJdxQcnUakShSbADhccx3xw28L2Nflo"


def the_work(script_folder, creds_path, geo_folder, **kwargs):

    credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_path)
    # If you copy this, make sure the file you are opening is accessible to your service account
    # Ie. Give Sharing/Edit access to ExProc (gdrive-user@exproc.iam.gserviceaccount.com)
    zip_spread = Spread(spread=gsheet_zip_link, creds=credentials)
    county_spread = Spread(spread=gsheet_county_link, creds=credentials)
    totals_spread = Spread(spread=gsheet_totals_link, creds=credentials)

    # Dates
    the_date = datetime.now(timezone('US/Central')).strftime("%m-%d")
    the_date_year_yday = datetime.strftime(datetime.now(timezone('US/Central')) - timedelta(1), '%m-%d-%y')
    the_date_year = datetime.now(timezone('US/Central')).strftime("%m-%d-%y")
    the_date_YEAR = datetime.now(timezone('US/Central')).strftime("%m-%d-%Y")
    the_date_n_time = datetime.now(timezone('US/Central')).strftime("%m-%d-%H%M")
    the_time = datetime.now(timezone('US/Central')).strftime("%H:%M")

    # Get the data in here
    df_county_today = county_spread.sheet_to_df(index=0, sheet=county_spread.find_sheet(the_date_year))
    df_county_yday = county_spread.sheet_to_df(index=0, sheet=county_spread.find_sheet(the_date_year_yday))
    df_county_today.set_index('County', inplace=True)
    df_county_yday.set_index('County', inplace=True)

    # Mapping datasets
    census_df = pd.read_csv(geo_folder / "Illinois_Census_200414_1816.csv")
    nofo_map_dict = dict(zip(census_df.CountyName, census_df.NOFO_Region))
    metro_map_dict = dict(zip(census_df.CountyName, census_df.Metro_area))

    # Calculate difference columns
    df_merge = df_county_today.merge(df_county_yday, how="left", left_index=True, right_index=True)
    df_merge.fillna(0, inplace=True)
    df_merge = df_merge.astype(int)
    df_merge['Tests_Diff'] = df_merge['Tested_x'] - df_merge['Tested_y']
    df_merge['Case_Diff'] = df_merge['Positive_Cases_x'] - df_merge['Positive_Cases_y']
    df_merge['Death_Diff'] = df_merge['Deaths_x'] - df_merge['Deaths_y']
    # Drop unneeded _y columns, rename _x columns into "Totals" Columns
    df_merge.drop(columns=['Positive_Cases_y', 'Deaths_y', 'Tested_y'], inplace=True)
    df_merge.rename(columns={'Tested_x': 'Total Tested', 'Positive_Cases_x': 'Total Cases', 'Deaths_x': 'Total Deaths'},
                    inplace=True)
    df_merge = df_merge[['Tests_Diff', 'Case_Diff', 'Death_Diff', 'Total Tested', 'Total Cases', 'Total Deaths']]
    # Fyi, there was a lot of trouble dealing with multiindex here. Don't do it on df_merge, do it individually below

    # Merge NOFO Regions into df_merge
    df_merge['NOFO Region'] = df_merge.index.map(nofo_map_dict)
    df_merge.loc[df_merge['NOFO Region'].isna(), "NOFO Region"] = df_merge.index[df_merge['NOFO Region'].isna()]

    # Merge Metro Areas into df_merge
    df_merge['Metro Area'] = df_merge.index.map(metro_map_dict)
    df_merge.loc['Chicago', 'Metro Area'] = 'Chicago'  # Is not mapped on its own in the mapping file.
    df_merge.loc['Illinois', 'Metro Area'] = 'Illinois'

    # Differences by County
    county_report = df_merge.copy()
    county_report.columns = pd.MultiIndex.from_tuples(
        [('Daily Difference', 'Tests'), ('Daily Difference', 'Cases'), ('Daily Difference', 'Deaths'),
         ('Totals to Date', 'Tests'), ('Totals to Date', 'Cases'), ('Totals to Date', 'Deaths'),
         ('Region', 'NOFO Region'), ('Region', 'Metro Area')])
    county_report_out = county_report.iloc[:, 0:9].to_string()
    print(county_report_out)

    # Differences by NOFO Region
    nofo_report = df_merge.copy().groupby(by="NOFO Region").sum()
    nofo_report.columns = pd.MultiIndex.from_product(
        [['Daily Difference', 'Totals to Date'], ['Tests', 'Cases', 'Deaths']])
    nofo_report_out = nofo_report.to_string()
    print(nofo_report_out)

    # Differences by Metro Area
    metro_report = df_merge.copy().groupby(by="Metro Area").agg("sum")
    metro_report.columns = pd.MultiIndex.from_product(
        [['Daily Difference', 'Totals to Date'], ['Tests', 'Cases', 'Deaths']])
    metro_report_out = metro_report.to_string()
    print(metro_report)

    with open(script_folder / "readme_template.md", "r") as rm_tmp:
        template = rm_tmp.read()
        new_readme = template.format(today_date_n_time=the_date_n_time,
                                     today_date=the_date_year,
                                     the_time=the_time,
                                     yday_date=the_date_year_yday,
                                     Metro_Report=metro_report,
                                     County_Report=county_report,
                                     NOFO_Report=nofo_report)

    with open(script_folder / "readme.md", "w+") as new_rm:
        new_rm.write(new_readme)
