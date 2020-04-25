# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 07:49:28 2020

@author: Mayank
"""


import pandas as pd
import numpy as np
import re
from  datetime import datetime as dt
import datetime

df1=pd.read_excel('outputcor.xlsx')
df2=pd.read_excel('output2.xlsx')
df3=pd.read_excel('output3.xlsx')
df4=pd.read_excel('output4.xlsx')
df5=pd.read_excel('output5.xlsx')


today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

actual_cols=[]
col_names=[]
for col in df2.columns:
    if re.match('Points',col):
        actual_cols.append(col[6:])
        col_names.append(col)
dict1={}
        
for i in range(len(actual_cols)):
    day = dt.strptime(actual_cols[i], '%Y-%m-%d')
    week=datetime.date(day.year, day.month, day.day).isocalendar()[1]
    if week not in dict1:
        dict1[week]=[col_names[i]]
    else:
        dict1[week].append(col_names[i])

active={}
for dataf in [df1,df2,df3,df4,df5]:
    for i in range(len(dataf)):
        for k,v in dict1.items():
            for col in v:
                try:
                    if dataf[col].iloc[i]!=0:
                        if k not in active:
                            active[k]=1
                        else:
                            active[k]+=1
                    break
                except: 
                    pass
                
df = pd.DataFrame(np.random.randint(0,100,size=(100, 4)), columns=list('ABCD'))
df.drop(columns=['A'])
df['Week']=0
df['WAU']=0

counter=0
for k,v in active.items():
    df['Week'].iloc[counter]='Week'+str(k)
    df['WAU'].iloc[counter]=v
    counter+=1
df=df.drop(columns=['A','B','C','D'])

df.to_excel('wau.xlsx',index=False)
    