# Nick's News Updater

Hello and welcome Illinois Covid-19 Researchers and Responders!

To facilitate your raw data needs, I am continually scraping and updating these google sheets with the numbers from the ILDPH Statistics front page.
The scraper automatically runs twice an hour at the 0015 and 0045 times. The sheets (linked below) only update when there are new results from ILDPH.
There are few hard data checks in place as the data is quite labile day to day, but size and shape of the data set are always ensured. 
(I am also manually checking everyday, at least through May.)

Please distribute as far and wide as you'd like!

[Illinois Totals Tracker](https://drive.google.com/open?id=1MWNebArAjjTTtJdxQcnUakShSbADhccx3xw28L2Nflo)

[Illinois Stats by Zip](https://drive.google.com/open?id=11P36C4z4B2vIXSfgchfAwWfLRnUD0zqg0Ki-MWCiC58)

[Illinois Stats by County](https://drive.google.com/open?id=1sbLLUOqEv_s2eOh3iQyWRw7JOB8rixfu1oBXgPy8zP8)

Please remember: These are all _raw_ numbers from the IDPH Website.

Cheers, Fg

## Most Recent Report - 04-22-20
##### Date Comparison: 04-22-20 and 04-21-20
###### (The numbers below are not absolute values. They are the direct result of subtracting values yesterdy's values from today's values. Ie, a positive number indicates a growth in count.)

By County

```
                          NOFO  Case_Diff  Death_Diff
County                                               
Greene                 Central          1           0
Macon                  Central         33           1
Macoupin               Central          2           0
Menard                 Central          1           0
Christian              Central          0           0
Logan                  Central          0           0
Cass                   Central          1           0
Morgan                 Central          1           0
Montgomery             Central          4           0
Sangamon               Central          1           0
Shelby                 Central          0           0
Chicago                Chicago        840          35
Kankakee                Collar          7           1
Kane                    Collar         80           4
Lake                    Collar         92           2
Grundy                  Collar          0           0
Will                    Collar         84           5
DuPage                  Collar         83           5
McHenry                 Collar         31           2
Kendall                 Collar         11           1
De Witt                De Witt          0           0
Illinois              Illinois       2049          97
LaSalle                LaSalle          5           0
McLean           North Central          0           0
Mason            North Central          1           0
Peoria           North Central          2           0
Stark            North Central          0           0
Tazewell         North Central         -5           0
Livingston       North Central          0           0
Marshall         North Central          0           0
Woodford         North Central          0           0
Fulton           North Central          0           0
Vermilion    Northeast Central          0           0
Douglas      Northeast Central          0           0
Iroquois     Northeast Central          0           0
Champaign    Northeast Central          0           0
Piatt        Northeast Central          0           0
Ford         Northeast Central          0           0
DeKalb                Northern          0           0
Stephenson            Northern          0           0
Boone                 Northern          6           0
Winnebago             Northern         31           0
Ogle                  Northern         12           0
Lee                  Northwest          1           0
Carroll              Northwest          0           0
Mercer               Northwest          0           0
Jo Daviess           Northwest          0           0
Rock Island          Northwest         25           1
Bureau               Northwest          0           0
Henry                Northwest          1           0
Whiteside            Northwest          3           0
Moultrie     Southeast Central          0           0
Richland     Southeast Central          0           0
Clark        Southeast Central          0           0
Clay         Southeast Central          1           0
Marion       Southeast Central         -1           0
Coles        Southeast Central          1           0
Lawrence     Southeast Central          0           0
Crawford     Southeast Central          1           0
Jasper       Southeast Central          0           0
Cumberland   Southeast Central          0           0
Effingham    Southeast Central          0           0
Fayette      Southeast Central          0           0
Hamilton              Southern          0           0
Saline                Southern          0           0
Alexander             Southern          0           0
Jefferson             Southern         41           1
Union                 Southern          0           0
Randolph              Southern          2           0
Pulaski               Southern          2           0
Hardin                Southern          0           0
Johnson               Southern          1           0
Wabash                Southern          0           0
Franklin              Southern          2           0
Wayne                 Southern          0           0
Gallatin              Southern          0           0
White                 Southern          0           0
Massac                Southern          0           0
Williamson            Southern          1           0
Perry                 Southern          1           0
Jackson               Southern          2           0
Bond         Southwest Central          0           0
Washington   Southwest Central          0           0
Madison      Southwest Central         36           3
Jersey       Southwest Central          0           0
Calhoun      Southwest Central          0           0
Monroe       Southwest Central          3           1
Clinton      Southwest Central          3           0
St. Clair    Southwest Central         27           1
Cook                  Suburban        525          35
Unassigned          Unassigned         36          -1
Henderson         West Central          0           0
Pike              West Central          0           0
Warren            West Central          4           0
Knox              West Central          5           0
McDonough         West Central          1           0
Hancock           West Central          0           0
Adams             West Central          0           0
Schuyler          West Central          0           0
```

By NOFO Regions

```
                   Case_Diff  Death_Diff
NOFO                                    
Central                   44           1
Chicago                  840          35
Collar                   388          20
De Witt                    0           0
Illinois                2049          97
LaSalle                    5           0
North Central             -2           0
Northeast Central          0           0
Northern                  49           0
Northwest                 30           1
Southeast Central          2           0
Southern                  52           1
Southwest Central         69           5
Suburban                 525          35
Unassigned                36          -1
West Central              10           0
```


### Notes:
On 4/18/2020, IDPH began to add a column for "Total Tested", the numbers for which on the first day are inconsistent with future uploads.
I have personally investigated my webscraper logs and have confirmed that this error was never corrected that day, but the numbers normalized the following day.
