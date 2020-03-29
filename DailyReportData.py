#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 09:44:25 2020

@author: toriyokoyama
"""

import pandas as pd
import numpy as np
from os import listdir
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

#%%

state_abbrev = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

state_abbrev_inv = {}
for k,v in state_abbrev.items():
    state_abbrev_inv[v] = k

#%%

path = '//home/toriyokoyama/Projects/covid19/csse_covid_19_data/csse_covid_19_daily_reports/'
files = [f for f in listdir(path) if '.csv' in f]
for i, file in enumerate(files):
    if i == 0:
        df = pd.read_csv(path + file)
        cols = df.columns
        df.columns = [col.replace('/','_').replace(' ','_').replace('Latitude','Lat').replace('Longitude','Long_') for col in cols]
        #df = df[(df['Country_Region']=='US')]
        df['File_Date'] = datetime.date(int(file[6:10]),int(file[0:2]),int(file[3:5]))
    else:
        new_df = pd.read_csv(path+file)
        cols = new_df.columns
        new_df.columns = [col.replace('/','_').replace(' ','_').replace('Latitude','Lat').replace('Longitude','Long_') for col in cols]
        #new_df = new_df[(new_df['Country_Region']=='US')]
        new_df['File_Date'] = datetime.date(int(file[6:10]),int(file[0:2]),int(file[3:5]))
        df = pd.concat((df,new_df),axis=0)
        
# extract date from datetime
df['Last_Update'] = pd.to_datetime(df['Last_Update']).dt.date
# fix some historical country labeling
df['Country_Region'].replace('China','Mainland China',inplace=True)
df['Country_Region'].replace('Korea, South','South Korea',inplace=True)
df['Country_Region'].replace('Republic of Korea','South Korea',inplace=True)
# fill county name with default value
df['Admin2'] = df['Admin2'].fillna('Unknown')
# get city/area and state from data
df['Province_State'] = df['Province_State'].fillna('')
df['City_Area'] = df['Province_State'].apply(lambda x: x.split(', ')).apply(lambda x: x[0] if len(x)==2 else '')
df['State'] = df['Province_State'].apply(lambda x: x.split(', ')).apply(lambda x: x[1] if len(x)==2 else x[0])
df['State'] = df['State'].apply(lambda x: state_abbrev_inv.get(x,x))
# make new key
df['Key'] = (df['Admin2'] + ', ' + df['City_Area'] + ', ' + df['State']).apply(lambda x: x[2:] if x[0:2]==', ' else (x[4:] if x[0:4]==', , ' else x))

#%%

groupByUS = df[df['Country_Region']=='US'].groupby(['File_Date']).sum()[['Confirmed','Deaths','Recovered']].reset_index()
groupByState = df[df['Country_Region']=='US'].groupby(['File_Date','State']).sum()[['Confirmed','Deaths','Recovered']].reset_index()
groupByAreaState = df[df['Country_Region']=='US'].groupby(['File_Date','City_Area','State']).sum()[['Confirmed','Deaths','Recovered']].reset_index()

groupByChina = df[df['Country_Region']=='Mainland China'].groupby(['File_Date']).sum()[['Confirmed','Deaths','Recovered']].reset_index()
groupBySKorea = df[df['Country_Region']=='South Korea'].groupby(['File_Date']).sum()[['Confirmed','Deaths','Recovered']].reset_index()
groupByItaly = df[df['Country_Region']=='Italy'].groupby(['File_Date']).sum()[['Confirmed','Deaths','Recovered']].reset_index()

#%%

plt.style.use('seaborn')
plt.fill_between('File_Date','Confirmed','Recovered',data=groupByChina,label='Confirmed')
plt.fill_between('File_Date','Recovered','Deaths',data=groupByChina,label='Recovered')
plt.fill_between('File_Date','Deaths',data=groupByChina,label='Deaths')
plt.xticks(rotation=45)
plt.xlabel('Date')
plt.legend(loc='best',frameon=True)
plt.title('Cumulative COVID-19 Statistics for China')
plt.show()

#%%

plt.style.use('seaborn')
plt.fill_between('File_Date','Confirmed','Recovered',data=groupByItaly,label='Confirmed')
plt.fill_between('File_Date','Recovered','Deaths',data=groupByItaly,label='Recovered')
plt.fill_between('File_Date','Deaths',data=groupByItaly,label='Deaths')
plt.xticks(rotation=45)
plt.xlabel('Date')
plt.legend(loc='best',frameon=True)
plt.title('Cumulative COVID-19 Statistics for Italy')
plt.show()

#%%

plt.style.use('seaborn')
plt.fill_between('File_Date','Confirmed','Recovered',data=groupBySKorea,label='Confirmed')
plt.fill_between('File_Date','Recovered','Deaths',data=groupBySKorea,label='Recovered')
plt.fill_between('File_Date','Deaths',data=groupBySKorea,label='Deaths')
plt.xticks(rotation=45)
plt.xlabel('Date')
plt.legend(loc='best',frameon=True)
plt.title('Cumulative COVID-19 Statistics for South Korea')
plt.show()

#%%

plt.style.use('seaborn')
plt.fill_between('File_Date','Confirmed','Recovered',data=groupByUS,label='Confirmed')
plt.fill_between('File_Date','Recovered','Deaths',data=groupByUS,label='Recovered')
plt.fill_between('File_Date','Deaths',data=groupByUS,label='Deaths')
plt.xticks(rotation=45)
plt.xlabel('Date')
plt.legend(loc='best',frameon=True)
plt.title('Cumulative COVID-19 Statistics for US')
plt.show()

#%%

plt.style.use('seaborn')
plt.fill_between('File_Date','Confirmed','Recovered',data=groupByAreaState[(groupByAreaState['State']=='IL') & (groupByAreaState['Confirmed']>0)],label='Confirmed')
plt.fill_between('File_Date','Recovered','Deaths',data=groupByAreaState[(groupByAreaState['State']=='IL') & (groupByAreaState['Confirmed']>0)],label='Recovered')
plt.fill_between('File_Date','Deaths',data=groupByAreaState[(groupByAreaState['State']=='IL') & (groupByAreaState['Confirmed']>0)],label='Deaths')
plt.xticks(rotation=45)
plt.xlabel('Date')
plt.legend(loc='best',frameon=True)
plt.title('Cumulative COVID-19 Statistics for Illinois')
plt.show()




# git merge upstream/master
