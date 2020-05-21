# Illinois Covid-19 Data Repeater

Hello Illinois Covid-19 Researchers and Responders,

To facilitate your raw data needs, I am continually scraping and updating these google sheets with the numbers from the IDPH Statistics front page.
The scraper automatically runs twice an hour at the 0015 and 0045 times. The sheets (linked below) only update when there are new results from IDPH.
These are all _raw_ numbers from the IDPH Website. I manually check the page and data everyday to ensure accuracy of my records (at least through May).

Please distribute freely.

[Illinois Totals Tracker](https://drive.google.com/open?id=1MWNebArAjjTTtJdxQcnUakShSbADhccx3xw28L2Nflo) | [csv](https://docs.google.com/spreadsheets/d/e/2PACX-1vTPKJQBxdcH_6Omx0RafPTtzOAct-dGKD_A3WNEGtCEVHlMQMvth0WmFVjZJROV1FBGHKwrTSgt17AV/pub?output=csv)

[Illinois Stats by Zip](https://drive.google.com/open?id=11P36C4z4B2vIXSfgchfAwWfLRnUD0zqg0Ki-MWCiC58) | [csv](https://docs.google.com/spreadsheets/d/e/2PACX-1vREg6fiLFxCxtR_SVLz7SHPoqJc7WSWnf4_tAx58Tk7_VZqdk0v0yVwIhHuouiuUbCQMDNtdJuH2Qhy/pub?output=csv)

[Illinois Stats by County](https://drive.google.com/open?id=1sbLLUOqEv_s2eOh3iQyWRw7JOB8rixfu1oBXgPy8zP8) | [csv](https://docs.google.com/spreadsheets/d/e/2PACX-1vSb9azvdy7HOiz7R4M_Z3ILxtw3Ns2mnt1qHhyTumlobNU3JXmTjRwUgu6fnPnKhMfrjJ7hKubbyIqR/pub?output=csv)

[Illinois Counties Covid-19 News Compiler](https://docs.google.com/spreadsheets/d/1Ik_Cyiv5Be4Cx-mCAf9jjNf1t4MVTmxqQeNesJjXhWY/)

Cheers, Fg

## Most Recent Report ({today_date_n_time})
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
On 4/18/2020, IDPH began to add a column for "Total Tested", the numbers for which on the first day are inconsistent with future uploads.
I have personally investigated my webscraper logs and have confirmed that this error was never corrected that day, but the numbers normalized the following day.

On 5/3/2020, I began scraping Google News to get a handle on the local news in our counties. That spreadsheet is also linked above.
