import sys
import time

from pathlib import Path
from datetime import datetime

import idph_stat_scraper_v2 as idph_stat_scraper
import report_maker
import git_committer

# Running on my own PC? Or Running headless on the RPi?
running_RPi = False


def launch_stat_scraper(running_on_RPi=False):
    print("\nLaunching IDPH Stat Scraper")
    things_changed = idph_stat_scraper.the_work(running_on_RPi)
    if things_changed:
        launch_report_maker(running_on_RPi)


def launch_report_maker(running_on_RPi=False):
    print("\nLaunching Report Maker")
    report_maker.the_work(running_on_RPi)
    print("\tUpdating and Pushing Git")
    git_committer.the_work()


if __name__ == "__main__":
    print(f"Arguments count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        print(f"Argument {i:>6}: {arg}")

    if "rpi" in sys.argv:
        running_RPi = True

    if "now" in sys.argv:
        launch_stat_scraper(running_RPi)

    while True:
        minutesToSleep = ((60 - datetime.now().minute) % 30) + 15
        print("Waiting %s minutes before running again." % minutesToSleep)
        time.sleep(60 * minutesToSleep)
        launch_stat_scraper(running_RPi)

# After pushing this to the main Git branch, here are the steps:
# Turn on RPi and get to terminal
# cd NicksNewsUpdater folder
# git fetch --all
# git reset --hard origin/master
# run it homie --> python3 idph_stats_scraper.py rpi
