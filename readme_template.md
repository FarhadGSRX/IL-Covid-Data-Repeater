# Illinois Covid-19 Data Repeater

Hello Illinois Covid-19 Researchers and Responders,

This repository contains data from the [IDPH website](http://www.dph.illinois.gov/covid19/covid19-statistics).  Data is collected daily to create a time series of statistics.  Some data labels on the site changed over time (eg. Confirmed Cases vs. Positive Cases), but similar data has been merged under the same headers here.

The scraper runs automatically. The sheets (linked below) only update when there are new results from IDPH.
These are all _raw_ numbers from the IDPH Website. 

Please distribute freely.

**NOTE:** We will try to keep this code running, but it is somewhat fragile, and it breaks with changes to the IDPH website.  A [new repository](https://github.com/cmaimone/idph_covid_data) that collects data from json files (instead of the rendered website), stores them in csv files (instead of google sheets), and includes demographic data and hospitalization statistics as well, is [available](https://github.com/cmaimone/idph_covid_data).  If there is something you're actively using in this repository that is missing from [the new one](https://github.com/cmaimone/idph_covid_data), [let Christina know](mailto:christina.maimone@norhtwestern.edu) and the new repository can likely be updated to accomodate the need.  **Please try to use the [new repository](https://github.com/cmaimone/idph_covid_data) instead.**


[Illinois Totals Tracker](https://drive.google.com/open?id=1MWNebArAjjTTtJdxQcnUakShSbADhccx3xw28L2Nflo) | [csv](https://docs.google.com/spreadsheets/d/e/2PACX-1vTPKJQBxdcH_6Omx0RafPTtzOAct-dGKD_A3WNEGtCEVHlMQMvth0WmFVjZJROV1FBGHKwrTSgt17AV/pub?output=csv)


[Illinois Stats by Zip - August 27, 2020 thru Now](https://drive.google.com/open?id=11P36C4z4B2vIXSfgchfAwWfLRnUD0zqg0Ki-MWCiC58) | [csv](https://docs.google.com/spreadsheets/d/e/2PACX-1vREg6fiLFxCxtR_SVLz7SHPoqJc7WSWnf4_tAx58Tk7_VZqdk0v0yVwIhHuouiuUbCQMDNtdJuH2Qhy/pub?output=csv)

[Illinois Stats by Zip - Start thru August 26, 2020](https://docs.google.com/spreadsheets/d/1s806jjVrGlejJkMtSSbjW7bh_LCmTYCiXujUTGhiv8o) | [csv](https://docs.google.com/spreadsheets/d/e/2PACX-1vS0ZfBggtLOJI1Upx6SEM2Ya0g6vWa8FWvKZPxIRtTtQnflQUk0khepTJMBTK9wbz_gtPyTwo5e2NSZ/pub?output=csv)


[Illinois Stats by County - August 27, 2020 thru Now](https://drive.google.com/open?id=1sbLLUOqEv_s2eOh3iQyWRw7JOB8rixfu1oBXgPy8zP8) | [csv](https://docs.google.com/spreadsheets/d/e/2PACX-1vSb9azvdy7HOiz7R4M_Z3ILxtw3Ns2mnt1qHhyTumlobNU3JXmTjRwUgu6fnPnKhMfrjJ7hKubbyIqR/pub?output=csv)

[Illinois Stats by County - Start thru August 26, 2020](https://docs.google.com/spreadsheets/d/1FByx9UUGQ4SLnUv8rZOFaji5F-KjoDcVu68vkU7ZJss) | [csv](https://docs.google.com/spreadsheets/d/e/2PACX-1vSlixXENtmT18YM4ZwZkoFSDeol4EZ9aV1iDJle6Q4BBQEaKUZKEQlRhRPR18KwdpenXaiopztY38HC/pub?output=csv)


[Illinois Counties Covid-19 News Compiler](https://docs.google.com/spreadsheets/d/1Ik_Cyiv5Be4Cx-mCAf9jjNf1t4MVTmxqQeNesJjXhWY/)

Cheers, Fg

## Most Recent Report ({the_date_year} {the_time})
##### Date Comparison: {today_date} and {yday_date}
###### (The numbers below are not absolute values. They are the direct result of subtracting yesterday's values from today's values. Ie, a positive number indicates a growth in count.)

By NOFO Regions

```
{NOFO_Report}
```

By Metro Areas
```
{Metro_Report}
```

By County

```
{County_Report}
```




### Notes:
Data for 10/31/2020 appears not to have posted to the IDPH site until 11/1/2020.  In the long-form data spreadsheets, the 10/31 entry has been manually updated to that day. - CM

Zip code testing data from 10/11/2020 is missing (the values are 0).  There is not a clear way to recover this from the IDPH website.  If anyone has this data, I can update the files. - CM

On 9/14/2020, "Positive Cases" on the IDPH website was relabelled "Confirmed Cases".  We're assuming these are equivalent and collecting the new data in the old columns. - CM

On 8/28/2020, I had to split up the increasingly large google sheets to avoid hitting the max number of tabs. Above this is reflected as more links to various subsets of the data. -FG

On 4/18/2020, IDPH began to add a column for "Total Tested", the numbers for which on the first day are inconsistent with future uploads.  I have personally investigated my webscraper logs and have confirmed that this error was never corrected that day, but the numbers normalized the following day.  -FG

On 5/3/2020, I began scraping Google News to get a handle on the local news in our counties. That spreadsheet is also linked above.  -FG

