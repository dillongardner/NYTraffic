# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 11:19:31 2016

@author: Dillon R. Gardner
"""

import requests
import pandas as pd
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

pageURL = "http://web.mta.info/developers/data/bandt/trafficdata.html"
soup = BeautifulSoup(pageStart.text)
xmlStub = "http://web.mta.info/developers/data/bandt/"

tmp = soup.find_all("div", class_="span-39 last")[0].find_all("a")[0]["href"]
xmlFile = requests.get(xmlStub + tmp)

root = ET.fromstring(xmlFile.text)

def extractDataFrameFromXML(xmlFile):
    ''' Convert XML file of MTA data to a DataFrame'''
    
    def dictionariesFromDay(day):
         dictionaries = []
         for child in day:
             newDict = child.attrib
             newDict.update(day.attrib)
             dictionaries.append(newDict)
         return(dictionaries)
       
    dictionaries = []
    for day in root:
        dictList = dictionariesFromDay(day)
        for newDict in dictList:
            dictionaries.append(newDict)
    df = pd.DataFrame(dictionaries, dtype=int)
    return(df)

def getXMLFiles():
    soup = BeautifulSoup(requests.get(pageURL).text)

