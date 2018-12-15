# coveredcalloptionsstrategy
Analyses the covered call strategy and prints a chart in comparison to direct investment


This Python script shows 4 charts. The first chart is the price chart of a stock in comparison to a 
chart with dividends included. The second is the same just in percentage.
The third and fourth chart show absolute and in percentage the covered call strategy in comparison to the price chart. One time a month
a Call Option out of the money is sold. How far out of the money can be adjusted with basisstdprc parameter.
If the price is higher than the Basis of the option of last month,
the difference is subtracted, because of expiration. If no 1 month options are available, the script
chooses 3 month options. The script sells at the open on expiration date (3. Friday of every month) the new option. 
If 3. Firday is holiday the script chooses the Thursday before.
Requirements to run this script:
Python 3.6
Packages:
pandas_datareader
matplotlib
numpy
pandas
mibian
datetime
