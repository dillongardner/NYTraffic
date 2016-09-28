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
xmlStub = "http://web.mta.info/developers/data/bandt/"


def extractDataFrameFromXML(xmlText):
    ''' Convert XML file of MTA data to a DataFrame'''
    
    def dictionariesFromDay(day):
         dictionaries = []
         for child in day:
             newDict = child.attrib
             newDict.update(day.attrib)
             dictionaries.append(newDict)
         return(dictionaries)
       
    root = ET.fromstring(xmlText)
    dictionaries = []
    for day in root:
        dictList = dictionariesFromDay(day)
        for newDict in dictList:
            dictionaries.append(newDict)
    df = pd.DataFrame(dictionaries, dtype=int)
    return(df)

def getXMLFiles():
    soup = BeautifulSoup(requests.get(pageURL).text, "lxml")
    xmlTag = soup.find("div", class_="span-39 last")
    xmlLinks = xmlTag.find_all("a")
    xmlList = []
    for link in xmlLinks:
        try:
            xmlRequest = requests.get(xmlStub + link["href"])
            xmlList.append(xmlRequest.text)
        except: 
            print("Error on file: " + link.text)
    return(xmlList)
    

xmlList = getXMLFiles()
df = pd.concat(map(extractDataFrameFromXML, xmlList))

