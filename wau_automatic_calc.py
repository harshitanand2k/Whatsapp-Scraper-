# -*- coding: utf-8 -*-
"""
Created on Wed May 13 18:47:26 2020

@author: Mayank
"""


import pandas as pd
import numpy as np
import re
from  datetime import datetime as dt
import datetime

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

actual_cols=[]
col_names=[]
for i in range(1,7):
    df=pd.read_excel('output'+str(i)+'.xlsx')
    for col in df.columns:
        if re.match('Points',col) and not re.search('.1',col):
            if col[6:] not in actual_cols:
                actual_cols.append(col[6:])
                col_names.append(col)
    actual_cols=list(actual_cols)
    dict1={}
    
for i in range(len(actual_cols)):
    day = dt.strptime(actual_cols[i], '%Y-%m-%d')
    week=datetime.date(day.year, day.month, day.day).isocalendar()[1]
    if week not in dict1.keys():
        dict1[week]=[actual_cols[i]]
    else:
        dict1[week].append(actual_cols[i])
        
df2=pd.read_excel('wau.xlsx')
kek=0
WAU=0
counter=0
for col in df2.columns:
    df2[col]=0


for i in range(1,7):
    df=pd.read_excel('output'+str(i)+'.xlsx')
    for k,v in dict1.items():
        for p in range(len(df)):
            for j in range(len(v)):
                try:
                    kek+= df['Points'+dict1[k][j]].iloc[p]
                except:
                    pass
            if kek!=0:
                WAU+=1
                kek=0
        df2['B'+str(i)].iloc[counter]=WAU
        counter+=1
        WAU=0
    counter=0
    

counter=0
for k,v in dict1.items():
    df2['A'].iloc[counter]='Week'+str(k)
    counter+=1


df2['B']=0
for i in range(len(df2)):
    for j in range(2,len(df2.columns)):
        df2['B'].iloc[i]+=df2[df2.columns[j]].iloc[i]
        

    