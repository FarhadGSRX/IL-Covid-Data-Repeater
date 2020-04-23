# Illinois Covid-19 Data Repeater

Hello and welcome Illinois Covid-19 Researchers and Responders!

To facilitate your raw data needs, I am continually scraping and updating these google sheets with the numbers from the IDPH Statistics front page.
The scraper automatically runs twice an hour at the 0015 and 0045 times. The sheets (linked below) only update when there are new results from IDPH.
There are few hard data checks in place as the data is quite labile day to day, but size and shape of the data set are always ensured. 
(I am also manually checking everyday, at least through May.)

Please distribute freely.

[Illinois Totals Tracker](https://drive.google.com/open?id=1MWNebArAjjTTtJdxQcnUakShSbADhccx3xw28L2Nflo)

[Illinois Stats by Zip](https://drive.google.com/open?id=11P36C4z4B2vIXSfgchfAwWfLRnUD0zqg0Ki-MWCiC58)

[Illinois Stats by County](https://drive.google.com/open?id=1sbLLUOqEv_s2eOh3iQyWRw7JOB8rixfu1oBXgPy8zP8)

Please remember: These are all _raw_ numbers from the IDPH Website.

Cheers, Fg

## Most Recent Report ({today_date_n_time})
##### Date Comparison: {today_date} and {yday_date}
###### (The numbers below are not absolute values. They are the direct result of subtracting yesterdy's values from today's values. Ie, a positive number indicates a growth in count.)

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
