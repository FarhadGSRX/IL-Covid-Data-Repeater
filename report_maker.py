# This script assumes that there is an update to report.
import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 10)

from gspread_pandas import Spread, Client
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
from pathlib import Path

# Running on my own PC? Or Running headless on the RPi?
running_RPi = False

# Paths
script_folder = Path("C:/Users/farha/Google Drive/XS/Git/NicksNewsUpdater/")
creds_path = "C:/Users/farha/Desktop/ExProc-Creds.json"

# All Google Auth and worksheet connection
idph_link = "http://www.dph.illinois.gov/covid19/covid19-statistics"

gsheet_zip_link = "https://docs.google.com/spreadsheets/d/11P36C4z4B2vIXSfgchfAwWfLRnUD0zqg0Ki-MWCiC58/edit#gid=0"
gsheet_county_link = "https://docs.google.com/spreadsheets/d/1sbLLUOqEv_s2eOh3iQyWRw7JOB8rixfu1oBXgPy8zP8/edit#gid=0"
gsheet_totals_link = "https://docs.google.com/spreadsheets/d/1MWNebArAjjTTtJdxQcnUakShSbADhccx3xw28L2Nflo/edit#gid=0"
idph_stats_zip_wksht_key = "11P36C4z4B2vIXSfgchfAwWfLRnUD0zqg0Ki-MWCiC58"
idph_stats_county_wksht_key = "1sbLLUOqEv_s2eOh3iQyWRw7JOB8rixfu1oBXgPy8zP8"
idph_stats_totals_wksht_key = "1MWNebArAjjTTtJdxQcnUakShSbADhccx3xw28L2Nflo"


def the_work(running_on_RPi=False):
    if running_on_RPi:
        script_folder = Path("/home/pi/Git/NicksNewsUpdater/")
        creds_path = "/home/pi/Git/Credentials/ExProc-Creds.json"
        backup_folder = Path(script_folder / "backup")
        idph_csv_folder = Path(script_folder / "idph_csv")
        geo_folder = Path(script_folder / "geo_data")
    else:
        script_folder = Path("C:/Users/farha/Google Drive/XS/Git/NicksNewsUpdater/")
        backup_folder = Path(script_folder / "backup")
        idph_csv_folder = Path(script_folder / "idph_csv")
        geo_folder = Path(script_folder / "geo_data")

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_path)
    # If you copy this, make sure the file you are opening is accessible to your service account
    # Ie. Give Sharing/Edit access to ExProc (gdrive-user@exproc.iam.gserviceaccount.com)
    zip_spread = Spread(spread=gsheet_zip_link, creds=credentials)
    county_spread = Spread(spread=gsheet_county_link, creds=credentials)
    totals_spread = Spread(spread=gsheet_totals_link, creds=credentials)

    # Dates
    the_date = datetime.now().strftime("%m-%d")
    the_date_year_yday = datetime.strftime(datetime.now() - timedelta(1), '%m-%d-%y')
    the_date_year = datetime.now().strftime("%m-%d-%y")
    the_date_YEAR = datetime.now().strftime("%m-%d-%Y")
    the_date_n_time = datetime.now().strftime("%m-%d-%H%M")
    the_time = datetime.now().strftime("%H:%M")

    # Mapping datasets
    census_df = pd.read_csv(geo_folder / "Illinois_Census_200414_1816.csv")
    nofo_map_dict = dict(zip(census_df.CountyName, census_df.NOFO_Region))
    metro_map_dict = dict(zip(census_df.CountyName, census_df.Metro_area))

    # Get the data in here
    df_county_today = county_spread.sheet_to_df(index=0, sheet=county_spread.find_sheet(the_date_year))
    df_county_yday = county_spread.sheet_to_df(index=0, sheet=county_spread.find_sheet(the_date_year_yday))
    df_county_today.set_index('County', inplace=True)
    df_county_yday.set_index('County', inplace=True)

    # dt_cols = ['update_date', 'update_time']
    # for col in dt_cols:
    #    df_county_today[col] = pd.to_datetime(df_county_today[col])
    #    df_county_yday[col] = pd.to_datetime(df_county_yday[col])

    df_merge = df_county_today.merge(df_county_yday, how="left", left_index=True, right_index=True)
    df_merge.fillna(0, inplace=True)
    df_merge['Case_Diff'] = df_merge['Positive_Cases_x'].astype(int) - df_merge['Positive_Cases_y'].astype(int)
    df_merge['Death_Diff'] = df_merge['Deaths_x'].astype(int) - df_merge['Deaths_y'].astype(int)

    df_merge['NOFO'] = df_merge.index.map(nofo_map_dict)
    df_merge.loc[df_merge.NOFO.isna(), "NOFO"] = df_merge.index[df_merge.NOFO.isna()]

    # Differences by County
    county_report = df_merge.sort_values(by="NOFO", ascending=True)[['NOFO', 'Case_Diff', 'Death_Diff']].to_string()
    print(county_report)

    print("\n")

    # Differences by NOFO Region
    nofo_report = df_merge.groupby(by="NOFO").agg("sum")[['Case_Diff', 'Death_Diff']].to_string()
    print(nofo_report)

    with open(script_folder / "readme_template.md", "r") as rm_tmp:
        template = rm_tmp.read()
        new_readme = template.format(today_date_n_time=the_date_n_time,
                                     today_date=the_date_year,
                                     yday_date=the_date_year_yday,
                                     County_Report=county_report,
                                     NOFO_Report=nofo_report)

    with open(script_folder / "readme.md", "w+") as new_rm:
        new_rm.write(new_readme)
