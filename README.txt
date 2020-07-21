This script uses JHU Covid19 data and US Census Bureau data to create bar graphs and disease, death, and population totals for states in the United States.

To call the function:
	covidplot("State")

**Update - 7/20/2020**
Another script is available to show Covid19 data for two states simultaneously. The first script was modified and the new script is called covid_statesx2.py.
To call the function:
	covidplot("State", "State")

**Update_2 - 7/21/2020**
Total number of people tested was obtained from the JHU GitHub Covid dataset and used for calculating number of confirmed out of number tested.

Resources:

Data import and data wrangling:
JHU Covid19 data on Github
https://github.com/CSSEGISandData


Analyzing Coronavirus (Covid-19) Data Using Pandas and Plotly
https://towardsdatascience.com/analyzing-coronavirus-covid-19-data-using-pandas-and-plotly-2e34fe2c4edc

Visualizing COVID-19 Data Beautifully in Python (in 5 Minutes or Less!!)
https://towardsdatascience.com/visualizing-covid-19-data-beautifully-in-python-in-5-minutes-or-less-affc361b2c6a


States Population data:
US Census Bureau
https://www.census.gov/data/tables/time-series/demo/popest/2010s-state-total.html