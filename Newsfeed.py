# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 13:20:41 2018

@author: ma
"""

import feedparser as fp
import json
from newspaper import Article
from time import mktime
import re
import pandas as pd
from gensim import corpora
from gensim.summarization.summarizer import summarize
import topic
import PolarityScore
import nltk
nltk.downloader.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
    
# Set the limit for number of articles to download for each link
LIMIT = 10

data = {}
data['newspapers'] = {}
df = pd.DataFrame(columns=['Headline','NewsUrl','Summary','Label','Theme','Relevance'])

with open('links.json') as data_file:
    companies = json.load(data_file)
    
# Loads the JSON files with news sites

textStr = ''
# Iterate through each news company
for company, value in companies.items():
    count = 1
    if True:
        newsPaper = {
            "articles": []}
        d = fp.parse(value['link'])
      
        for entry in d.entries:
           if hasattr(entry, 'published') and count<LIMIT:
                article = {}
                date = entry.published_parsed
                try:
                    content = Article(entry.link)
                    content.download()
                    content.parse()
                except Exception as e:
                    print(e)
                    print("continuing...")
                    continue
                article['Headline'] = content.title
                article['NewsUrl'] = content.url
                article['Summary'] = summarize(content.text,ratio=0.2)
                article['Label']= company
                quoted = re.compile('"[^"]*"')
                topicstr = ''
                strTpc = topic.findTopic(article['Summary'])
                for value in quoted.findall(str(strTpc)):
                    topicstr = topicstr+value
                article['Theme'] = topicstr.replace('"'," ")
                article['Relevance'] = PolarityScore.findScore(content.text)
                duplicate = False
                for val in df['Theme']:
                    if val == article['Theme']:
                        duplicate = True
                        break
                if not duplicate:
                    df = df.append(article,ignore_index=True)
                    count = count + 1
       
writer = pd.ExcelWriter('output.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()

