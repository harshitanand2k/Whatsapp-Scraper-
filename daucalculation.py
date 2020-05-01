# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 04:40:39 2020

@author:Snorlax/Kinjaz/Harhsit
"""

import pandas as pd
import numpy as np
import datetime

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

df = pd.DataFrame(np.random.randint(0,100,size=(100, 4)), columns=list('ABCD'))

df=df.drop(columns=['B','C','D'])
counter=0
for i in range(35,0,-1):
    day=today - datetime.timedelta(days=i)
    name='Points'+str(day)
    df['A'].iloc[counter]=name
    counter+=1
    

for i in range(1,6):
    df2=pd.read_excel('output'+str(i)+'.xlsx')
    active=0
    for j in range(len(df)):
        if df['A'].iloc[j] in df2.columns:
            for k in range(len(df2)):
                if df2[df['A'].iloc[j]].iloc[k]!=0:
                    active+=1
            df['Group'+str(i)].iloc[j]=active
            active=0
        


df.to_excel('dau.xlsx',index=False)



























