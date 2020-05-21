import time
import sys
import argparse
from pathlib import Path
from datetime import datetime
import shutil

from selenium import webdriver

import idph_stat_scraper as idph_stat_scraper
import report_maker
import git_committer


def launch_stat_scraper(chrome_options, config):
    print("\nLaunching IDPH Stat Scraper")
    things_changed = idph_stat_scraper.the_work(chrome_options=chrome_options, **config)
    if things_changed:
        launch_report_maker(**config)


def launch_report_maker(config):
    print("\nLaunching Report Maker")
    report_maker.the_work(**config)
    print("\tUpdating and Pushing Git")
    git_committer.the_work(**config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Collect COVID data for Illinois')
    parser.add_argument('--rpi', action='store_true',
                        help='include if running on Raspberry Pi?')
    parser.add_argument('--farhadlocal', action='store_true',
                        help="include if running on Farhad's local machine")
    parser.add_argument('--notnow', action='store_true',
                        help='include to avoid running immediately')
    parser.add_argument('--future', action='store_true',
                        help='include to run this at :15 and :45 past the hour')
    parser.add_argument('--reportonly', action='store_true',
                        help='only run the report maker')
    args = parser.parse_args()

    config = dict()
    chrome_options = webdriver.ChromeOptions()
    if args.rpi:
        config['script_folder'] = Path("/home/pi/Git/NicksNewsUpdater/")
        config['creds_path'] = "/home/pi/Git/Credentials/ExProc-Creds.json"
        config['backup_folder'] = Path(config['script_folder'] / "backup")
        config['idph_csv_folder'] = Path(config['script_folder'] / "idph_csv")
        config['geo_folder'] = Path(config['script_folder'] / "geo_data")
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--window-size=1024,768")
        chrome_options.add_argument("--test-type")
    elif args.farhadlocal:
        config['script_folder'] = Path("C:/Users/farha/Google Drive/XS/Git/NicksNewsUpdater/")
        config['creds_path'] = "C:/Users/farha/Desktop/ExProc-Creds.json"
        config['backup_folder'] = Path(config['script_folder'] / "backup")
        config['idph_csv_folder'] = Path(config['script_folder'] / "idph_csv")
        config['geo_folder'] = Path(config['script_folder'] / "geo_data")
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument("--test-type")
    else:
        config['script_folder'] = Path(".")
        config['creds_path'] = "creds.json"
        config['backup_folder'] = Path("backup")
        config['idph_csv_folder'] = Path("idph_csv")
        config['geo_folder'] = Path("geo_data")
        config['chrome_path'] = shutil.which('chromedriver')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--window-size=1024,768")
        chrome_options.add_argument("--test-type")
        chrome_options.add_argument("--no-sandbox")

    if args.reportonly:
        launch_report_maker(config)
        sys.exit()

    # Run it now
    if not args.notnow:
        launch_stat_scraper(chrome_options, config)

    # Keep it running every 30 minutes
    while args.future:
        minutesToSleep = ((60 - datetime.now().minute) % 30) + 15
        print("Waiting %s minutes before running again." % minutesToSleep)
        time.sleep(60 * minutesToSleep)
        launch_stat_scraper(chrome_options, config)


