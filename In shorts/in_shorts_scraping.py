# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 13:21:08 2020

@author: vignesh
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import numpy as np
from dateutil.parser import parse
import matplotlib.pyplot as plt
import seaborn as sns
import os

seed_urls = ['https://inshorts.com/en/read/technology',
             'https://inshorts.com/en/read/sports',
             'https://inshorts.com/en/read/world',
             'https://inshorts.com/en/read/entertainment',
             'https://inshorts.com/en/read/business']

def build_dataset(seed_urls):
    news_data = []
    for url in seed_urls:
        news_category = url.split('/')[-1]
        data = requests.get(url)
        soup = BeautifulSoup(data.content, 'html.parser')
        
        news_articles = [{'Heading': headline.find('span', 
                                                         attrs={"itemprop": "headline"}).string,
                          'Summary': article.find('div', 
                                                       attrs={"itemprop": "articleBody"}).string,
                          'news_date': date.find('span', 
                                                       attrs={"clas": "date"}).string,
                          'Link': headline.find('a')['href'], 
                          'Category': news_category.capitalize()}
                         
                            for headline, article, date in 
                             zip(soup.find_all('div', 
                                               class_=["news-card-title news-right-box"]),
                                 soup.find_all('div', 
                                               class_=["news-card-content news-right-box"]),
                                 soup.find_all('div',
                                               class_=["news-card-author-time news-card-author-time-in-title"]))
                        ]
        
        news_data.extend(news_articles)
        
    df =  pd.DataFrame(news_data)
    datetimesplit=df['news_date'].str.split(",", n=1, expand=True)
    df['Date']=datetimesplit[0]
    df['Day']=datetimesplit[1]
    df.drop(columns=["news_date"],inplace=True)
    
        #date[i]=parse(date[i]).strftime('%Y/%m/%d')
    for i in range(len(df['Date'])):
        df['Date'][i]=datetime.datetime.strptime(df['Date'][i], '%d %b %Y').strftime('%Y-%m-%d')
    df['Timestamp']=df['Date'].str.cat(df['Day'],sep=",")
    df = df[['Heading', 'Summary', 'Category','Link','Timestamp']]
    return df

news_df = build_dataset(seed_urls)
news_df.to_csv("./Dataset/inshorts_2020-06-17.csv")