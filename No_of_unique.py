# -*- coding: utf-8 -*-
"""
Created on Fri May  1 08:01:39 2020

@author: Mayank
"""


import pandas as pd
import numpy as np
import datetime
from collections import defaultdict

dict1=defaultdict()
for i in range(1,6):
    df2=pd.read_excel('PointsTablemid'+str(i)+'.xlsx')
    for i in range(len(df2)):
        if df2['Number'].iloc[i] not in dict1:
            dict1[df2['Number'].iloc[i]]=0

print(len(dict1))