# -*- coding: utf-8 -*-
"""
Created on Wed May 20 17:03:21 2020

@author: HP
"""


# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 19:50:36 2020
@author: Snorlax / Kinjaz / Harshit
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
from selenium.webdriver.chrome.options import Options
from selenium import webdriver




def initiator():
    """
    
    Initializing a selenium object which is the key for initiating the scraper
    Its just a basic chrome window which can be automated  using methods provided by selenium library
    """
    
    driver = Chrome()
    driver.get('https://web.whatsapp.com/')
    time.sleep(60)
    
    return driver





def scroller(group,driver):
    """
    Parameters
    ----------
    group : TYPE - name of the group
        DESCRIPTION - It's to be used as we have to find the title of the group and click it open'
    Returns
   
    soup- The beautiful soup object
     """
    driver.find_element_by_class_name('C28xL').click()
    entername=driver.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/div/div[2]')
    entername.send_keys(str(group))
    hoja=False
    
    while hoja==False:
        try:
            driver.find_element_by_xpath('//*[@title='+'"'+str(group)+'"'+']').click()
            hoja=True
        except:
            pass
    try:
        driver.find_element_by_class_name('_2pyvj').click()
    except:
        pass
    time.sleep(60)
    please=False
    while please==False:
        try:
            driver.find_element_by_xpath('//*[@id="side"]/div[1]/div/button').click()
            please=True
        except:
            pass    
    reg=r'MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY'
    elements=driver.find_elements_by_class_name('Tkt2p')
    elem=elements[0]
    var=True
    checked=[]
    while var: 
        try:
            driver.execute_script("arguments[0].scrollIntoView();", elem)
            elements=driver.find_elements_by_class_name('Tkt2p')
            elem=elements[0]
            driver.implicitly_wait(0.0000000000000000000000000001)
        except:
            elements=driver.find_elements_by_class_name('Tkt2p')
            elem=elements[0]
            driver.implicitly_wait(0.0000000000000000000000000001)
        try:
            kek=driver.find_elements_by_class_name('_3FXB1')
            for i in range(len(kek)):
                if kek[i] not in checked:
                    if re.search(reg,kek[i].text):
                        var=False
                    else:
                        checked.append(kek[i])
        except:
            pass
        
    sourcer=(driver.page_source).encode('utf-8')
    from bs4 import BeautifulSoup
    soup=BeautifulSoup(sourcer,features='html.parser')   
    return soup
    




def computation_names(soup):
    """
    
    Parameters
    ----------
    soup : the beautiful soup object
        DESCRIPTION.- 
    group_no : the group no( i.e 1,2, 3)
    
        DESCRIPTION. - This is the syntax with respect to whcih i Have made the 
                        data files , like output1, output2
    Returns
    
    names: dictionary
        DESCRIPTION - The list of numbers , with the number of total likes they got
                        and the songs they posted
    """    
    
    times=soup.findAll("span",{"class":"_3EFt_"})
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
                            if link not in names[k] :
                                names[k].append(link)
        else:
            for i in range(len(initial_msg)):
                if initial_msg[i:i+11]=='https://you':
                    link=initial_msg[i:i+28]
                    for k,v in names.items():
                        if link in v:
                            names[k][0]+=1
                            
    p=driver.find_element_by_class_name('_2y17h')
    q=p.find_element_by_xpath('div[2]/div[2]/span')
    l=q.text
    l=l.split(',')
    for i in range(len(l)):
        l[i]=l[i].replace(" ","")
        l[i]=l[i][3:]
    
    popper=[]
    for k,v in names.items():
        if k not in l:
            popper.append(k)
        
    for item in popper:
        names.pop(item)
                        
    return names





def computation_links(soup,names):
    """
    Parameters
    ----------
    soup : The beautiful soup object
        DESCRIPTION :
    group_no : Integer
        DESCRIPTION - the gorup number synatx , to be used 
    names : TYPE - dictionary
        DESCRIPTION - the dictionary containing names
    Returns
    links: TYPE -dictionary
        DESCRIPTION - the dictionary containing links
        
    """
    
    links=defaultdict()
    lol_new=soup.findAll("div",{"class":"Tkt2p"})
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
    return(links)



def compute_output_file(names,group_no):
    
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
                    if str(group_no)=='1':
                        if int(df['No_Of_Songs'+str(yesterday)].iloc[i])<=3:
                            df['Points'+str(yesterday)].iloc[i]=(((len(names[k]))-1)*15)
                        else:
                            df['Points'+str(yesterday)].iloc[i]=3*15
                            
                    else:
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
                    if str(group_no)=='1':
                        df['Points'+str(yesterday)].iloc[i]=(((len(names[k]))-1)*15)
                        print('group1 different point system active')
                    else:
                        
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
    print('output file written')
    return(df)


def compute_outputer_file(links,group_no):
       
    df2 = pd.read_excel("outputer"+str(group_no)+".xlsx")
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
    return df2
    

def compute_pointstable_file(names,group_no,df):
        
    df3=pd.read_excel('PointsTablemid'+str(group_no)+'.xlsx',dtype={'Number':str})
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
    df3.to_excel('PointsTablemid'+str(group_no)+'.xlsx',index=False)
    print('df3 written')
    return df3


def sender_boi(driver,df3,group):
    driver.find_element_by_xpath('//*[@title='+'"'+str(group)+'"'+']').click()
    for i in range(len(df3)):
        if df3['Number'].iloc[i]==str(0):
            df3=df3.iloc[:i+2,:]
            break
    ans=df3.to_string()
    entername=driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
    entername.send_keys(str(ans))
    driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]').clear()
        



list_of_groups=['Leaf song discovery Hindi','Leaf SongDiscoveryHindi 2','Leaf SongDiscoveryHindi 3','Leaf SongDiscoveryHindi 4','Leaf SongDiscoveryHindi 5']
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
for group in list_of_groups:
    if list_of_groups.index(group)+1==1:
        driver=initiator()
    soup=scroller(group,driver)
    soup2=soup
    names=computation_names(soup)
    links=computation_links(soup2,names)
    df=compute_output_file(names,str(list_of_groups.index(group)+1))
    df2=compute_outputer_file(links,list_of_groups.index(group)+1)
    df3=compute_pointstable_file(names,list_of_groups.index(group)+1,df)
    sender_boi(driver,df3,group)
    