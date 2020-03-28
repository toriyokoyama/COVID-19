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

groupByUS = df[df['Country_Region']=='US'].groupby(['File_Date','Last_Update']).sum()[['Confirmed','Deaths','Recovered']].reset_index()
groupByUS_NoDup = groupByUS[groupByUS.duplicated(['Last_Update'])==False]
groupByState = df[df['Country_Region']=='US'].groupby(['File_Date','Last_Update','State']).sum()[['Confirmed','Deaths','Recovered']].reset_index()
groupByState_NoDup = groupByState[groupByState.duplicated(['Last_Update','State'])==False]
groupByAreaState = df[df['Country_Region']=='US'].groupby(['File_Date','Last_Update','City_Area','State']).sum()[['Confirmed','Deaths','Recovered']].reset_index()
groupByAreaState_NoDup = groupByAreaState[groupByAreaState.duplicated(['Last_Update','City_Area','State'])==False]

groupByChina = df[df['Country_Region']=='Mainland China'].groupby(['File_Date','Last_Update']).sum()[['Confirmed','Deaths','Recovered']].reset_index()
groupByChina_NoDup = groupByChina[groupByChina.duplicated(['Last_Update'])==False]
groupBySKorea = df[df['Country_Region']=='South Korea'].groupby(['File_Date','Last_Update']).sum()[['Confirmed','Deaths','Recovered']].reset_index()
groupBySKorea_NoDup = groupBySKorea[groupBySKorea.duplicated(['Last_Update'])==False]

#%%

plt.style.use('seaborn')
x = groupByUS_NoDup[(groupByUS_NoDup['Confirmed']>1)]['File_Date']
y = groupByUS_NoDup[(groupByUS_NoDup['Confirmed']>1)][['Confirmed','Deaths','Recovered']]
plt.stackplot(x,y.values.T,labels=['Confirmed','Deaths','Recovered'])
plt.xticks(rotation=45)
plt.legend()
plt.show()

#%%

plt.style.use('seaborn')
x = groupByState_NoDup[(groupByState_NoDup['State']=='IL') & (groupByState_NoDup['Confirmed']>1)]['File_Date']
y = groupByState_NoDup[(groupByState_NoDup['State']=='IL') & (groupByState_NoDup['Confirmed']>1)][['Confirmed','Deaths','Recovered']]
plt.stackplot(x,y.values.T,labels=['Confirmed','Deaths','Recovered'])
plt.xticks(rotation=45)
plt.legend()
plt.show()

# git merge upstream/master