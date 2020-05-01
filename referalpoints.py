# -*- coding: utf-8 -*-
"""
Created on Fri May  1 08:42:11 2020

@author: Mayank
"""


import pandas as pd
import numpy as np
import datetime
from collections import defaultdict


df=pd.read_excel('referal.xlsx')
df2=pd.read_excel('PointsTablemid3.xlsx')
for i in range(len(df)):
    for j in range(len(df2)):
        if str(df['Number2'].iloc[i])==str(df2['Number'].iloc[j]):
            df2['Points'].iloc[j]+=50
            
df2.to_excel('PointsTablemid3.xlsx',index=False)