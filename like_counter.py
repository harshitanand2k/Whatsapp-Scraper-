# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 14:29:23 2020

@author: HP
"""


import pandas as pd
import numpy as np
import re
from  datetime import datetime as dt
import datetime

df = pd.DataFrame(np.random.randint(0,100,size=(100, 4)), columns=list('ABCD'))

df=df.drop(columns=['B','C','D'])
counter=0
for i in range(40,0,-1):
    day=today - datetime.timedelta(days=i)
    name='No of Likes'+str(day)
    df['A'].iloc[counter]=name
    counter+=1
    
for i in range(1,8):
    df['Group'+str(i)]=0
    
for i in range(1,8):
    df2=pd.read_excel('outputer'+str(i)+'.xlsx')
    likes=0
    for j in range(len(df)):
        if df['A'].iloc[j] in df2.columns:
            for k in range(len(df2)):
                likes+=df2[df['A'].iloc[j]].iloc[k]
                df['Group'+str(i)].iloc[j]=likes
            likes=0
            
for i in range(len(df)):
    df['A'].iloc[i]=str(df['A'].iloc[i])[6:]
    df['A'].iloc[i]=str(df['A'].iloc[i])[5:]
df.to_excel('no_of_likes.xlsx',index=False)