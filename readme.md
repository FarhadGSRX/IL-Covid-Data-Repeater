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

## Most Recent Report (11-04-20 12:48)
##### Date Comparison: 11-04-20 and 11-03-20
###### (The numbers below are not absolute values. They are the direct result of subtracting yesterday's values from today's values. Ie, a positive number indicates a growth in count.)

By NOFO Regions

```
                  Daily Difference              Totals to Date               
                             Tests Cases Deaths          Tests   Cases Deaths
NOFO Region                                                                  
Central                       2087   293      8         329182   15317    270
Chicago                      11226  1387     17        1604274  108570   3101
Collar                       14920  2180      9        1612488  108641   2206
Illinois                     71857  7538     55        8030713  437556   9933
North Central                 3665   379      2         385833   16585    241
Northeast Central            13955   195      0         933427   11238     89
Northern                      2520   408      1         264766   20447    283
Northwest                     2165   352      6         221410   14447    265
Out Of State                   308     0      0          56663       1      0
Southeast Central              659   155      1         128584    9246    195
Southern                       971   109      2         171984   12256    260
Southwest Central             2010   257      0         275879   21382    489
Suburban                     11967  1605      7        1400087   92606   2440
Unassigned                     318    12      0          65370      53      0
West Central                   940   206      2         110003    6755     94
```

By Metro Areas
```
                  Daily Difference              Totals to Date               
                             Tests Cases Deaths          Tests   Cases Deaths
Metro Area                                                                   
Bloomington                   1565    94      0         114973    4976     44
Cape_Girardeau                   5     1      0           2555     157      2
Carbondale-Marion              351    42      1          59161    3893     90
Champaign-Urbana             13309   127      0         865852    7656     48
Chicago                      31644  4216     31        3944846  262350   6780
Danville                       388    45      0          39959    2081     12
Davenport                      832   133      0         109321    6093    111
Decatur                        336    29      2          59387    3890     66
Elgin                         3087   421     -1         296936   22653    402
Illinois                     71857  7538     55        8030713  437556   9933
Kankakee                       777   119      2          72748    4116     83
Lake                          3138   475      1         352606   23652    525
Peoria                        1537   222      2         226731    9680    171
Rockford                      1577   268      0         173367   14543    221
Springfield                    909   121      0         150378    5200     67
St_Louis                      2123   280      0         295271   21936    498
```

By County

```
             Daily Difference              Totals to Date                 \
                        Tests Cases Deaths          Tests   Cases Deaths   
County                                                                     
Illinois                71857  7538     55        8030713  437556   9933   
Adams                     191    80      0          42110    2426     26   
Alexander                   5     1      0           2555     157      2   
Bond                       30    10      0           8305     576      9   
Boone                     203    53      0          24174    2285     26   
Brown                      26    11      0           2460     144      0   
Bureau                    186    24      0          14375    1079     19   
Calhoun                    27     8      0           1846      94      0   
Carroll                    82    12      1           8074     571     15   
Cass                       34     3      0           6090     481     11   
Champaign               13084   115      0         845735    7114     29   
Chicago                 11226  1387     17        1604274  108570   3101   
Christian                  67    36      0          15307     978     31   
Clark                      13    11      0           5793     349     18   
Clay                       15     3      0           4808     366     15   
Clinton                   117    22      0          19359    1988     32   
Coles                     114    42      0          29010    2271     42   
Cook                    11967  1605      7        1400087   92606   2440   
Crawford                    9     1      0           6354     690      6   
Cumberland                 18     3      0           4843     333      6   
De Witt                    52     2      0           6641     314      6   
DeKalb                    533    59      0          50287    2954     43   
Douglas                    78    15      0          12209     868      9   
DuPage                   3511   553      6         460250   27065    632   
Edgar                      17     5      0           5254     190     11   
Edwards                    15     0      0           1218     119      0   
Effingham                 117    18      0          15884    1403      5   
Fayette                    16    21      0           8603     783     24   
Ford                      130     3      0           8265     231     16   
Franklin                   80    10      0          17614    1151     11   
Fulton                    308    37      0          17314     728      2   
Gallatin                   10     1      0           1200     123      2   
Greene                     33     9      1           5319     365     18   
Grundy                    216    52      0          15944    1227      8   
Hamilton                   28     0      0           2279     155      2   
Hancock                    22    13      0           7518     408      4   
Hardin                      1     1      0           1458      62      0   
Henderson                   9     8      0           2246     153      0   
Henry                     280    12      0          23009     926      9   
Iroquois                  180     8      0          15407     633     20   
Jackson                   157    15      0          24771    1713     26   
Jasper                     13     5      0           3762     306     10   
Jefferson                 106    16      0          14446    1052     52   
Jersey                    112     4      0           9040     521     21   
Jo Daviess                146    13      1           8406     617     10   
Johnson                    80     3      0           4481     420      0   
Kane                     2554   362     -1         246649   19699    359   
Kankakee                  777   119      2          72748    4116     83   
Kendall                   611   103      0          48483    3331     30   
Knox                      361    34      1          26323    1543     23   
Lake                     3138   475      1         352606   23652    525   
LaSalle                   583    60      0          43572    2997     70   
Lawrence                   92     8      0           7338     393      8   
Lee                        93    24      0          12353     997      4   
Livingston                218    24      0          20062     827     12   
Logan                      80    19      1          19987     724      5   
Macon                     336    29      2          59387    3890     66   
Macoupin                  145    26      0          23869     919     11   
Madison                   792   128      0         106744    8108    163   
Marion                    128    25      0          20693    1263     25   
Marshall                   59     3      0           6249     184      4   
Mason                      37     2      0           6753     374     12   
Massac                     19     3      0           3611     184      2   
McDonough                 212    18      0          14540     876     21   
McHenry                  1661   140      0         112382    7756    120   
McLean                   1513    92      0         108332    4662     38   
Menard                     41     2      0           6465     198      1   
Mercer                     61     6      0           7028     368      7   
Monroe                     60    16      0          12228    1112     34   
Montgomery                366    19      0          18982     725     17   
Morgan                     81    11      0          17516    1110     26   
Moultrie                   53     8      1           7761     534      7   
Ogle                      221    32      0          22000    1555      8   
Out Of State              308     0      0          56663       1      0   
Peoria                    813   120      2         118165    5337     87   
Perry                      33     2      0           8194     536     16   
Piatt                      95     9      0          11852     311      3   
Pike                       45    16      1           6182     486      9   
Pope                       10     2      0            886      49      1   
Pulaski                     2     0      0           2222     255      1   
Putnam                     29     3      0           1759     118      0   
Randolph                   75     5      1          16963    1450     16   
Richland                   54     5      0           8481     365     18   
Rock Island               491   115      0          79284    4799     95   
Saline                     80     9      0           9064     682     11   
Sangamon                  868   119      0         143913    5002     66   
Schuyler                    9     3      0           2420     109      1   
Scott                       7     1      0           2999     122      0   
Shelby                     29    19      4           9348     803     18   
St. Clair                 840    66      0         113880    8618    228   
Stark                      25     3      0           3039     102      3   
Stephenson                189    49      1          19112    1395     11   
Tazewell                  494    69      0          80218    3213     60   
Unassigned                318    12      0          65370      53      0   
Union                      30     2      0           9526     837     25   
Vermilion                 388    45      0          39959    2081     12   
Wabash                      4     6      0           3184     271      6   
Warren                     65    23      0           6204     610     10   
Washington                 32     3      0           4477     365      2   
Wayne                       9     5      0           5958     555     18   
White                      33     1      0           7964     305      5   
Whiteside                 214    83      4          23550    1975     36   
Will                     2452   376      1         303426   21795    449   
Williamson                194    27      1          34390    2180     64   
Winnebago                1374   215      0         149193   12258    195   
Woodford                  146    27      0          19060     844     17   

                         Region                     
                    NOFO Region         Metro Area  
County                                              
Illinois               Illinois           Illinois  
Adams              West Central                NaN  
Alexander              Southern     Cape_Girardeau  
Bond          Southwest Central           St_Louis  
Boone                  Northern           Rockford  
Brown              West Central                NaN  
Bureau                Northwest                NaN  
Calhoun       Southwest Central           St_Louis  
Carroll               Northwest                NaN  
Cass                    Central                NaN  
Champaign     Northeast Central   Champaign-Urbana  
Chicago                 Chicago            Chicago  
Christian               Central                NaN  
Clark         Southeast Central                NaN  
Clay          Southeast Central                NaN  
Clinton       Southwest Central           St_Louis  
Coles         Southeast Central                NaN  
Cook                   Suburban            Chicago  
Crawford      Southeast Central                NaN  
Cumberland    Southeast Central                NaN  
De Witt           North Central        Bloomington  
DeKalb                 Northern              Elgin  
Douglas       Northeast Central                NaN  
DuPage                   Collar            Chicago  
Edgar         Southeast Central                NaN  
Edwards                Southern                NaN  
Effingham     Southeast Central                NaN  
Fayette       Southeast Central                NaN  
Ford          Northeast Central   Champaign-Urbana  
Franklin               Southern                NaN  
Fulton            North Central                NaN  
Gallatin               Southern                NaN  
Greene                  Central                NaN  
Grundy                   Collar            Chicago  
Hamilton               Southern                NaN  
Hancock            West Central                NaN  
Hardin                 Southern                NaN  
Henderson          West Central                NaN  
Henry                 Northwest          Davenport  
Iroquois      Northeast Central                NaN  
Jackson                Southern  Carbondale-Marion  
Jasper        Southeast Central                NaN  
Jefferson              Southern                NaN  
Jersey        Southwest Central           St_Louis  
Jo Daviess            Northwest                NaN  
Johnson                Southern                NaN  
Kane                     Collar              Elgin  
Kankakee                 Collar           Kankakee  
Kendall                  Collar            Chicago  
Knox               West Central                NaN  
Lake                     Collar               Lake  
LaSalle               Northwest                NaN  
Lawrence      Southeast Central                NaN  
Lee                   Northwest                NaN  
Livingston        North Central                NaN  
Logan                   Central                NaN  
Macon                   Central            Decatur  
Macoupin                Central           St_Louis  
Madison       Southwest Central           St_Louis  
Marion        Southeast Central                NaN  
Marshall          North Central             Peoria  
Mason             North Central                NaN  
Massac                 Southern                NaN  
McDonough          West Central                NaN  
McHenry                  Collar            Chicago  
McLean            North Central        Bloomington  
Menard                  Central        Springfield  
Mercer                Northwest          Davenport  
Monroe        Southwest Central           St_Louis  
Montgomery              Central                NaN  
Morgan                  Central                NaN  
Moultrie      Southeast Central                NaN  
Ogle                   Northern                NaN  
Out Of State       Out Of State                NaN  
Peoria            North Central             Peoria  
Perry                  Southern                NaN  
Piatt         Northeast Central   Champaign-Urbana  
Pike               West Central                NaN  
Pope                   Southern                NaN  
Pulaski                Southern                NaN  
Putnam                Northwest                NaN  
Randolph               Southern                NaN  
Richland      Southeast Central                NaN  
Rock Island           Northwest          Davenport  
Saline                 Southern                NaN  
Sangamon                Central        Springfield  
Schuyler           West Central                NaN  
Scott                   Central                NaN  
Shelby                  Central                NaN  
St. Clair     Southwest Central           St_Louis  
Stark             North Central             Peoria  
Stephenson             Northern                NaN  
Tazewell          North Central             Peoria  
Unassigned           Unassigned                NaN  
Union                  Southern                NaN  
Vermilion     Northeast Central           Danville  
Wabash                 Southern                NaN  
Warren             West Central                NaN  
Washington    Southwest Central                NaN  
Wayne                  Southern                NaN  
White                  Southern                NaN  
Whiteside             Northwest                NaN  
Will                     Collar            Chicago  
Williamson             Southern  Carbondale-Marion  
Winnebago              Northern           Rockford  
Woodford          North Central             Peoria  
```




### Notes:
Data for 10/31/2020 appears not to have posted to the IDPH site until 11/1/2020.  In the long-form data spreadsheets, the 10/31 entry has been manually updated to that day. - CM

Zip code testing data from 10/11/2020 is missing (the values are 0).  There is not a clear way to recover this from the IDPH website.  If anyone has this data, I can update the files. - CM

On 9/14/2020, "Positive Cases" on the IDPH website was relabelled "Confirmed Cases".  We're assuming these are equivalent and collecting the new data in the old columns. - CM

On 8/28/2020, I had to split up the increasingly large google sheets to avoid hitting the max number of tabs. Above this is reflected as more links to various subsets of the data. -FG

On 4/18/2020, IDPH began to add a column for "Total Tested", the numbers for which on the first day are inconsistent with future uploads.  I have personally investigated my webscraper logs and have confirmed that this error was never corrected that day, but the numbers normalized the following day.  -FG

On 5/3/2020, I began scraping Google News to get a handle on the local news in our counties. That spreadsheet is also linked above.  -FG

