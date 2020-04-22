# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 19:50:36 2020

@author: Mayank
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
from collections import defaultdict 


#initiating the selenium object
driver = Chrome()
driver.get('https://web.whatsapp.com/')




def scroller(group):
    driver.find_element_by_xpath('//*[@title='+'"'+str(group)+'"'+']').click()

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
        
        sourcer=(driver.page_source).encode('utf-8')
        from bs4 import BeautifulSoup
        soup=BeautifulSoup(sourcer,features='html.parser')
        
        return soup
    


def computation_output(soup,group_no):
    times=soup.findAll("span",{"class":"_3EFt_"})
    #all the messages
    lol_new=soup.findAll("div",{"class":"Tkt2p"})
    
    sender_msg_numbers=soup.findAll("span",{"class":"RZ7GO"})
    names=defaultdict()
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
    df = pd.read_excel('output'+str(group_no)+'.xlsx',dtype={'Name':str})
    
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
    df.to_excel("output"+str(group_no)+".xlsx",index=False)
    return names



def compute_outputer(soup,group_no,names):
    links=defaultdict()
    lol_new=soup.findall("div",{"class":"Tkt2p"})
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
                            
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    df2 = pd.read_excel('outputer'+str(group_no)+'.xlsx')
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

    df2.to_excel("outputer"+str(group_no)+".xlsx",index=False)
    return links

    
    


list_of_groups=['Leaf SongDiscoveryHindi 3']

for group in list_of_groups:
    soup=scroller(group)
    names=computation_output(soup,list_of_groups.index(group)+1)
    links=computation_outputer(soup,list_of_groups.index(group)+1,names)
    computation_points_table(list_of_groups.index(group)+1,names)
    
    