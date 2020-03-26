# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 13:54:48 2020

@author: HP
"""

import requests
from selenium.webdriver import Chrome
import numpy as np
import pandas as pd
import pyautogui
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import re
import datetime

#initiating the selenium object
driver = Chrome()
driver.get('https://web.whatsapp.com/')

#finding and opening the specific group
driver.find_element_by_xpath('//*[@title="Leaf song discovery Hindi"]').click()
driver.find_element_by_class_name('_1ays2')
reg=r'MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY'

#initializing elem as the first elem to be the first message on the html page
elements=driver.find_elements_by_class_name('-N6Gq')
elem=elements[0]
var=True
checked=[]
while var:
    #using the elem object to scroll up the table 
    driver.execute_script("arguments[0].scrollIntoView();", elem)
    elements=driver.find_elements_by_class_name('-N6Gq')
    elem=elements[0]
    driver.implicitly_wait(0.0000000000000000000000000001)
    
    try:
        #finding the tag of today , yesterday , monday , wed etc
        kek=driver.find_elements_by_class_name('_F7Vk')
        for i in range(len(kek)):
            if kek[i] not in checked:
                if re.search(reg,kek[i].text):
                    print('found')
                    var=False
                else:
                    checked.append(kek[i])
                    
                    
                
    except:
        pass




# creating a bs4 object to parse the page
sourcer=(driver.page_source).encode('utf-8')
from bs4 import BeautifulSoup
soup=BeautifulSoup(sourcer,features='html.parser')


from collections import defaultdict 
import re
times=soup.findAll("span",{"class":"_3fnHB"})
#all the messages
lol_new=soup.findAll("div",{"class":"-N6Gq"})

# to find the messages specific to yesterday
start_end=[]
for i in range(len(times)-1):
    if re.search('PM',times[i].get_text()) and re.search('AM',times[i+1].get_text()):
        start_end.append(i)
        print(times[i].get_text(),times[i+1].get_text())
lol_new=lol_new[start_end[0]:start_end[1]]

#populating the names of the sen
sender_msg_numbers=soup.findAll("span",{"class":"ZObjg"})
names=defaultdict()
links=defaultdict()
for name in sender_msg_numbers:
    if name.get_text() not in names.keys():
        k=name.get_text()[4:]
        names[k]=[0]
        



for badmsg in lol_new:
    msg=badmsg.get_text()[4:]
    if re.search('www.youtube.com',msg,re.IGNORECASE):
        for k,v in (names.items()):    
            if re.match(k,msg,re.IGNORECASE):
                for j in range(len(msg)):
                    if msg[j:j+11]=='https://you':
                        link=msg[j:j+28]
                        if link not in names[k] and len(names[k])<4:
                            names[k].append(link)
    else:
        for i in range(len(msg)):
            if msg[i:i+11]=='https://you':
                link=msg[i:i+28]
                for k,v in names.items():
                    if link in v:
                        names[k][0]+=1
                        


                        
                        
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
df = pd.read_excel('output.xlsx')

df['Count'+str(yesterday)]=0
df['No_Of_Songs'+str(yesterday)]=0
df['Song_Link'+str(yesterday)]=0
df['Points'+str(yesterday)]=0

for k,v in names.items():
    if k in df.Name.unique():
        for i in range(len(df)):
            if df['Name'].iloc[i]==k:
                df['Count'+str(yesterday)].iloc[i]=names[k][0]
                try:
                    df['Song_Link'+str(yesterday)].iloc[i]=names[k][1:]
                except:
                    df['Song_Link'+str(yesterday)].iloc[i]=0
                df['No_Of_Songs'+str(yesterday)].iloc[i]=len(names[k])-1
                df['Points'+str(yesterday)].iloc[i]=((len(names[k])-1)*3)+(names[k][0])
    else:
        for i in range(len(df)):
            if df['Name'].iloc[i]==0:
                df['Name'].iloc[i]=k
                df['Count'+str(yesterday)].iloc[i]=names[k][0]
                try:
                    df['Song_Link'+str(yesterday)].iloc[i]=names[k][1:]
                except:
                    df['Song_Link'+str(yesterday)].iloc[i]=0
                df['No_Of_Songs'+str(yesterday)].iloc[i]=len(names[k])-1
                df['Points'+str(yesterday)].iloc[i]=((len(names[k])-1)*3)+(names[k][0])
                break

df['Count'+str(yesterday)].iloc[len(df)-1]=0
df['Count'+str(yesterday)].iloc[len(df)-1]=df['Count'+str(yesterday)].sum()
df['No_Of_Songs'+str(yesterday)].iloc[len(df)-1]=0
df['No_Of_Songs'+str(yesterday)].iloc[len(df)-1]=df['No_Of_Songs'+str(yesterday)].sum() 
df['Points'+str(yesterday)].iloc[len(df)-1]=0
df['Points'+str(yesterday)].iloc[len(df)-1]=df['Points'+str(yesterday)].sum()      
df['Name'].iloc[len(df)-1]='Sums of all fields'              
df.to_excel("output{}.xlsx".format(str(yesterday)),index=False)

for msg in lol_new:
    print(msg.get_text())    


for badmsg in lol_new:
    msg=badmsg.get_text()[4:]
    if re.search('www.youtube.com',msg,re.IGNORECASE):
        for k,v in (names.items()):    
            if re.match(k,msg,re.IGNORECASE):
                for j in range(len(msg)):
                    if msg[j:j+11]=='https://you':
                        link=msg[j:j+28]
                        links[link]=[0]
                        links[link].append(msg[:11])
    else:
        for i in range(len(msg)):
            if msg[i:i+11]=='https://you':
                link=msg[i:i+28]
                for k,v in links.items():
                    if link==k:
                        links[k][0]+=1

df2 = pd.DataFrame(np.random.randn(100, 4), columns=list('ABCD'))
df2['links']=0
df2['No of Likes']=0
df2['Shared By']=0

counter=0
for k,v in links.items():
    df2['links'].iloc[counter]=k
    df2['No of Likes'].iloc[counter]=links[k][0]
    df2['Shared By'].iloc[counter]=links[k][1]
    counter+=1
df2=df2.drop(['A','B','C','D'],axis=1)
print(df2)
df2.to_excel("outputer.xlsx")