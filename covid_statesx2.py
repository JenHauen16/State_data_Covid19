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

def covidplot(state, state2):
    date1 = "1/22/20"
    date2 = date.today() - timedelta(days=2)
    #for strftime, need to use - to get rid of leading zero for linux/mac and use # for windows
    mydates = pd.date_range(date1, date2).strftime("%-m/%-d/%y").tolist()
    col_names = ["Date", "Cases"]
    codf1 = pd.DataFrame(columns=col_names)
    
    #state
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
    deathrate_state = round((death_total/confirm_total)*100, 2)



    #state2
    codf2 = pd.DataFrame(columns=col_names)
    for index, x in enumerate(mydates):
        try:
            s = int(pd.Series(abs(usconfirmstates.loc[state2, mydates[index + 1]]["Cases"].sum() - usconfirmstates.loc[state2, x]["Cases"].sum())))
            codf2 = codf2.append(pd.DataFrame([{"Date": x, "Cases" : s}]), ignore_index=True)
        except IndexError:
            continue
    print(codf2)
    confirm_total2 = usconfirmstates.loc[state2, (date.today()- timedelta(days=2)).strftime("%-m/%-d/%y")]["Cases"].sum() 
    print("Total Confirmed Cases for " + state2 + " is " + str(confirm_total2))
    
    codeaths2 = pd.DataFrame(columns=col_names)
    for index, y in enumerate(mydates):
        try:
            ss = int(pd.Series(abs(usdstates.loc[state2, mydates[index + 1]]["Cases"].sum() - usdstates.loc[state2, y]["Cases"].sum())))
            codeaths2 = codeaths2.append(pd.DataFrame([{"Date": y, "Cases" : ss}]), ignore_index=True)
        except IndexError:
            continue
    print(codeaths2)                               
    death_total2 = usdstates.loc[state2, (date.today()- timedelta(days=2)).strftime("%-m/%-d/%y")]['Cases'].sum()
    print("Total Deaths for " + state2 + " is " + str(death_total2))

    #get value only for cell of dataframe use .values[0]
    pop2 = state_pop.loc[state_pop['State'] == state2, 'Population'].values[0]
    percon2 = round((confirm_total2/pop2)*100, 2)
    perdeath2 = round((death_total2/pop2)*100, 2)
    deathrate_state2 = round((death_total2/confirm_total2)*100, 2)



    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, figsize=(9,5))
    #state
    ax1.bar(codf1["Date"], codf1["Cases"], color="red")
    #ax1.set_xlabel("Date")
    ax1.set_xticks(codf1["Date"][::7])
    ax1.get_xaxis().set_visible(False)
    #ax1.set_xticklabels(codf1["Date"][::7], rotation=90)
    ax1.set_ylabel("Cases")
    ax1.set_title("{} Total Confirmed = {:,} - {}%".format(state, confirm_total, percon))
    ax2.bar(codeaths["Date"], codeaths["Cases"], color="black")
    #ax2.set_xlabel("Date")
    ax2.set_xticks(codeaths["Date"][::7])
    ax2.get_xaxis().set_visible(False)
    #ax2.set_xticklabels(codeaths["Date"][::7], rotation=90, fontsize=3)
    ax2.set_ylabel("Cases")
    ax2.set_title("{} Total Deaths = {:,} - {}%".format(state, death_total, deathrate_state))

    #state2
    ax3.bar(codf1["Date"], codf2["Cases"], color="red")
    ax3.set_xlabel("Date")
    ax3.set_xticks(codf2["Date"][::7])
    ax3.set_xticklabels(codf2["Date"][::7], rotation=90)
    ax3.set_ylabel("Cases")
    ax3.set_title("{} Total Confirmed = {:,} - {}%".format(state2, confirm_total2, percon2))
    ax4.bar(codeaths2["Date"], codeaths2["Cases"], color="black")
    ax4.set_xlabel("Date")
    ax4.set_xticks(codeaths2["Date"][::7])
    ax4.set_xticklabels(codeaths2["Date"][::7], rotation=90)
    ax4.set_ylabel("Cases")
    ax4.set_title("{} Total Deaths = {:,} - {}%".format(state2, death_total2, deathrate_state2))

    

    plt.suptitle('Covid19 data for {} and {} Since January 22, 2020. \nTotal population of {} is {:,} and {} is {:,}.'.format(state, state2, state, pop, state2, pop2))
    plt.show()

covidplot("Georgia", "Florida")

