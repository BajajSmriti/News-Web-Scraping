# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 21:47:18 2020

@author: Smriti
"""

# Importing libraries

from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime


### API for get requests

categoryList=['world','technology','arts','sports','business']
responseList=[]
for i in categoryList:
    link="https://www.nytimes.com/section/"+i
    print(link)
    responseList.append(requests.get(link))


### Fetching attributes   
    
heading=[] #List to store the heading of the article
link=[] #List to store the article's href
summary=[] #List to store the summary of the article
category=[]#List to store the category of the article
timestampList=[]
todaysDate = datetime.today().strftime('%Y-%m-%d')

for x,response in enumerate(responseList):
    soup = BeautifulSoup(response.content,"html.parser") #Using BeautifulSoup class for the html parser 
    a = soup.find_all('article')
    for i in a:
        head=i.find('h2')
        if(head!=None):
            if(head.text!=" "):
                heading.append(head.text)
                if(x==2):
                    category.append('Entertainment')
                else:
                    category.append(categoryList[x].capitalize())
                link1=i.find('a')
                if(link1!=None):
                    link.append(link1['href'])
                    if(not link1['href'][1:5].isnumeric()):
                        timestampList.append(todaysDate)
                    elif('/'in link1['href'][1:11]):
                        temp=link1['href'][1:11].replace('/','-')
                        timestampList.append(temp)
                ptag=i.find('p')
                if(ptag!=None):
                    summary.append(ptag.text)
                elif(i.find('ul')!=None):
                    summary.append(i.find('ul').text)
                else:
                    summary.append("None")    
print(heading[0],len(heading))
print(link[5],len(link))
print(summary[8],len(summary))
print(timestampList[5],len(timestampList))


### Time column modified

for i in range(len(timestampList)):
    day=datetime.strptime(timestampList[i], '%Y-%m-%d').strftime('%A')
    timestampList[i]=(timestampList[i]+","+day)        
print(timestampList[7],len(timestampList))


### Cleaning unsupported variables

def replaceFunc(j):
    for i in range(len(j)):
        if('‘' in j[i]):
            j[i]=j[i].replace('‘',"'")
        if('“'in j[i]):
            j[i]=j[i].replace('“',"'")
        if('’' in j[i]):
            j[i]=j[i].replace('’',"'")
        if('”'in j[i]):
            j[i]=j[i].replace('”',"'")
        if('—'in j[i]):
            j[i]=j[i].replace('—','-')
    
x = [heading, summary]
for i in x:
    replaceFunc(i)

    
### Storing attributes in a csv
    
filename='Dataset/nyt_'+todaysDate+'.csv'
print(filename)
df = pd.DataFrame({'Heading':heading,'Summary':summary,'Category':category,'Link':link,'Timestamp':timestampList}) 
df.to_csv(filename, index=False, encoding='utf-8')

