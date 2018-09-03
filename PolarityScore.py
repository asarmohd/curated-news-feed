# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 19:55:57 2018

@author: ma
"""
#created wn dictionary of stock market related words to calculate the score
def findScore(text):
    file1 = open("Stock_Words.txt","r+")
    textarray = []
    words = []
    fileText = file1.read()
    for t in str.split(text," "):
        textarray.append(t)

    Score = 0          
    for word in str.split(fileText,','):
        word.replace("'","")
        words.append(word)
    
    for tex in textarray:
        for word in words:
            if tex.lower().strip() == word.lower().strip():
                if Score<50:
                    Score += 50  
                elif Score<75:
                    Score += 2
                elif Score<100:
                    Score += 1

    return Score


