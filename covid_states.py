import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from datetime import date, timedelta, datetime
pd.set_option('display.max_columns', None)


usconfirm_raw=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
usdeaths_raw=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv')
state_pop=pd.read_excel('/Users/jenniferhauenstein/Documents/covid_scripts/US_States_Covid19_Bar_Graphs/State_Populations.xlsx')

usconfirm_sub=usconfirm_raw.iloc[1:,5:]
usdeaths_sub=usdeaths_raw.iloc[1:,5:]

def cleandataus(df_raw):
    df_cleaned=df_raw.melt(id_vars=['Admin2','Province_State','Country_Region','Lat','Long_', 'Combined_Key'],value_name='Cases',var_name='Date')
    df_cleaned=df_cleaned.set_index(['Admin2','Province_State','Date'])
    return df_cleaned
usconfirm=cleandataus(usconfirm_sub)
usdeaths=cleandataus(usdeaths_sub)

usconfirm_states= usconfirm
usd=usdeaths

usreset=usconfirm_states.reset_index()
usdreset=usd.reset_index()

del usreset['Admin2']
del usdreset['Admin2']

usconfirmstates=usreset.set_index(["Province_State", "Date"])
usdstates=usdreset.set_index(["Province_State", "Date"])

def covidplot(state):
    date1 = "1/22/20"
    date2 = date.today() - timedelta(days=2)
    #for strftime, need to use - to get rid of leading zero for linux/mac and use # for windows
    mydates = pd.date_range(date1, date2).strftime("%-m/%-d/%y").tolist()
    col_names = ["Date", "Cases"]
    codf1 = pd.DataFrame(columns=col_names)
    for index, x in enumerate(mydates):
        try:
            s = int(pd.Series(abs(usconfirmstates.loc[state, mydates[index + 1]]["Cases"].sum() - usconfirmstates.loc[state, x]["Cases"].sum())))
            codf1 = codf1.append(pd.DataFrame([{"Date": x, "Cases" : s}]), ignore_index=True)
        except IndexError:
            continue
    print(codf1)
    confirm_total = usconfirmstates.loc[state, (date.today()- timedelta(days=2)).strftime("%-m/%-d/%y")]["Cases"].sum() 
    print("Total Confirmed Cases for " + state + " is " + str(confirm_total))
    
    codeaths = pd.DataFrame(columns=col_names)
    for index, y in enumerate(mydates):
        try:
            ss = int(pd.Series(abs(usdstates.loc[state, mydates[index + 1]]["Cases"].sum() - usdstates.loc[state, y]["Cases"].sum())))
            codeaths = codeaths.append(pd.DataFrame([{"Date": y, "Cases" : ss}]), ignore_index=True)
        except IndexError:
            continue
    print(codeaths)                               
    death_total = usdstates.loc[state, (date.today()- timedelta(days=2)).strftime("%-m/%-d/%y")]['Cases'].sum()
    print("Total Deaths for " + state + " is " + str(death_total))

    #get value only for cell of dataframe use .values[0]
    pop = state_pop.loc[state_pop['State'] == state, 'Population'].values[0]
    percon = round((confirm_total/pop)*100, 2)
    perdeath = round((death_total/pop)*100, 2)
    
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(9,5))
    ax1.bar(codf1["Date"], codf1["Cases"], color="red")
    ax1.set_xlabel("Date")
    ax1.set_xticks(codf1["Date"][::7])
    ax1.set_xticklabels(codf1["Date"][::7], rotation=90)
    ax1.set_ylabel("Cases")
    ax1.set_title("Confirmed Covid19 Since January 22, 2020 \n Total Confirmed = {:,} - {}%".format(confirm_total, percon))
    ax2.bar(codeaths["Date"], codeaths["Cases"], color="black")
    ax2.set_xlabel("Date")
    ax2.set_xticks(codeaths["Date"][::7])
    ax2.set_xticklabels(codeaths["Date"][::7], rotation=90)
    ax2.set_ylabel("Cases")
    ax2.set_title("Deaths Covid19 Since January 22, 2020 \n Total Deaths = {:,} - {}%".format(death_total, perdeath))

    plt.suptitle('Covid19 data for {}. Total Population of {} is {:,}.'.format(state, state, pop))
    plt.show()

covidplot("Georgia")

