# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 17:53:38 2020

@author: HP
"""

import requests
from selenium.webdriver import Chrome
import numpy as np
import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import re
import datetime

#initiating the selenium object
driver = Chrome()
driver.get('https://web.whatsapp.com/')

#finding and opening the specific group
driver.find_element_by_xpath('//*[@title="Leaf SongDiscoveryHindi 3"]').click()

reg=r'MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY'

#initializing elem as the first elem to be the first message on the html page
elements=driver.find_elements_by_class_name('Tkt2p')
elem=elements[0]
var=True
checked=[]
while var:
    #using the elem object to scroll up the table 
    driver.execute_script("arguments[0].scrollIntoView();", elem)
    elements=driver.find_elements_by_class_name('Tkt2p')
    elem=elements[0]
    driver.implicitly_wait(0.0000000000000000000000000001)
    
    try:
        #finding the tag of today , yesterday , monday , wed etc
        kek=driver.find_elements_by_class_name('_3FXB1')
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
times=soup.findAll("span",{"class":"_3EFt_"})
#all the messages
lol_new=soup.findAll("div",{"class":"Tkt2p"})

# to find the messages specific to yesterday
start_end=[]
for i in range(len(times)-1):
    if re.search('PM',times[i].get_text()) and re.search('AM',times[i+1].get_text()):
        start_end.append(i)
        print(times[i].get_text(),times[i+1].get_text())
lol_new=lol_new[start_end[0]:start_end[1]]

#populating the names of the sen
sender_msg_numbers=soup.findAll("span",{"class":"RZ7GO"})
names=defaultdict()
links=defaultdict()
for name in sender_msg_numbers:
    k=name.get_text().replace(" ","")
    if '-' in k:
        k=k.replace("-","")
        k=k.replace("(","")
        k=k.replace(")","")
    if k not in names.keys():
        k=k[len(k)-10:]
        names[k]=[0]
        



for badmsg in lol_new:
    initial_msg=badmsg.get_text()
    msg=initial_msg
    msg=msg.replace(" ","")
    msg=msg.replace("-","")
    msg=msg.replace(")","")
    msg=msg.replace("(","")
    if msg[1]=="1":
        msg=str(msg[2:12])
    else:
        msg=str(msg[3:13])
    print(msg)
    if re.search('www.youtube.com',initial_msg,re.IGNORECASE):
        for k,v in (names.items()):    
            if re.match(k,msg,re.IGNORECASE):
                for j in range(len(initial_msg)):
                    if initial_msg[j:j+11]=='https://you':
                        link=initial_msg[j:j+28]
                        if link not in names[k] and len(names[k])<4:
                            names[k].append(link)
    else:
        for i in range(len(initial_msg)):
            if initial_msg[i:i+11]=='https://you':
                link=initial_msg[i:i+28]
                for k,v in names.items():
                    if link in v:
                        names[k][0]+=1
                        


                        
                        
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
df = pd.read_excel('output3copy.xlsx',dtype={'Name':str})

df['Count'+str(yesterday)]=0
df['No_Of_Songs'+str(yesterday)]=0
df['Song_Link'+str(yesterday)]=0
df['Points'+str(yesterday)]=0

for k,v in names.items():
    if k in df.Name.unique():
        for i in range(len(df)):
            if str(df['Name'].iloc[i])==str(k):
                df['Count'+str(yesterday)].iloc[i]=names[k][0]
                try:
                    df['Song_Link'+str(yesterday)].iloc[i]=names[k][1:]
                except:
                    df['Song_Link'+str(yesterday)].iloc[i]=0
                df['No_Of_Songs'+str(yesterday)].iloc[i]=len(names[k])-1
                df['Points'+str(yesterday)].iloc[i]=((len(names[k])-1)*3)+(names[k][0])
    else:
        for i in range(len(df)):
            if df['Name'].iloc[i]=='0':
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
df.to_excel("output3copy.xlsx",index=False)

   


for badmsg in lol_new:
    l=badmsg.get_text().replace(" ","")
    if '-' in l:
        l=l.replace("-","")
        l=l.replace("(","")
        l=l.replace(")","")
    l=l[3:]
    if re.search('www.youtube.com',l,re.IGNORECASE)!=None:
        for k,v in (names.items()):    
            if re.match(k,l,re.IGNORECASE):
                for j in range(len(l)):
                    if l[j:j+11]=='https://you':
                        link=l[j:j+28]
                        links[link]=[0]
                        links[link].append(l[:11])
    else:
        for i in range(len(l)):
            if l[i:i+11]=='https://you':
                link=l[i:i+28]
                for k,v in links.items():
                    if link==k:
                        links[k][0]+=1
                        links[k].append(l[0:10])

df2 = pd.read_excel('outputer3.xlsx')
df2['links'+str(yesterday)]=0
df2['No of Likes'+str(yesterday)]=0
df2['Shared By'+str(yesterday)]=0
df2['Liked By'+str(yesterday)]=0

counter=0
for k,v in links.items():
    df2['links'+str(yesterday)].iloc[counter]=k
    df2['No of Likes'+str(yesterday)].iloc[counter]=links[k][0]
    df2['Shared By'+str(yesterday)].iloc[counter]=links[k][1]
    try:
        df2['Liked By'+str(yesterday)].iloc[counter]=links[k][2:]
    except:
        df2['Liked By'+str(yesterday)].iloc[counter]=0
    counter+=1



df2.to_excel("outputer3.xlsx",index=False)


luldict=defaultdict()

    
for badmsg in lol_new:
    msg=badmsg.get_text()[4:]
    print(msg)
    if re.search('www.youtube.com',msg,re.IGNORECASE):
        pass
    else:
        number=msg[0:11]
        for i in range(len(msg)):
            if msg[i]=='+':
                name=msg[11:i]
        luldict[number]=name

df3=pd.read_excel('PointsTablemid3copy.xlsx',dtype={'Number':str})
for k,v in names.items():
    if k not in df3['Number'].unique():
        for i in range(len(df3)):
            if df3['Number'].iloc[i]=='0':
                df3["Number"].iloc[i]=k
                break
                
for i in range(len(df3)):
    for j in range(len(df)):
        if df['Name'].iloc[j]==df3['Number'].iloc[i]:
            df3['Points'].iloc[i]+=df["Points"+str(yesterday)].iloc[j]
            break
        

df3.to_excel('PointsTablemid3copy.xlsx',index=False)
countlol=0
for i in range(len(df)):
    if df['Name'].iloc[i]!='0':
        if df["Points"+str(yesterday)].iloc[i]!=0:
            countlol+=1
print('The number of active users for ' + str(yesterday) +' are ' + str(countlol) +' (group 2)')
print('The number of links shared on ' + str(yesterday) +' are ' + str(len(links)) + '(group 2)')
