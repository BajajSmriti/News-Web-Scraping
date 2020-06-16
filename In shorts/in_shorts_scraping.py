# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 13:21:08 2020

@author: vignesh
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
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
        
        news_articles = [{'news_headline': headline.find('span', 
                                                         attrs={"itemprop": "headline"}).string,
                          'news_article': article.find('div', 
                                                       attrs={"itemprop": "articleBody"}).string,
                          'news_date': date.find('span', 
                                                       attrs={"clas": "date"}).string,
                          'news_time': date.find('span', 
                                                       attrs={"class": "time"}).string,
                          'news_link': headline.find('a')['href'], 
                          'news_category': news_category}
                         
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
    df['news_timestamp']=df['news_date'].str.cat(df['news_time'],sep=" ")
    df = df[['news_headline', 'news_article', 'news_category','news_timestamp','news_link']]
    return df

news_df = build_dataset(seed_urls)
news_df.to_csv("inshorts_16_06_2020.csv")