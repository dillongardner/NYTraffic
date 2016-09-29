# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 11:19:31 2016

Downloads XML data files from trafffic at 
http://web.mta.info/developers/data/bandt/trafficdata.html

Formats and saves the data to a feather file

If run as a script, will accept and arguement for the location of the feather
files

@author: Dillon R. Gardner
"""

import requests
import feather
import os
import sys
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
       
    try: 
        root = ET.fromstring(xmlText)
        dictionaries = []
        for day in root:
            dictList = dictionariesFromDay(day)
            for newDict in dictList:
                dictionaries.append(newDict)
        df = pd.DataFrame(dictionaries, dtype=int)
    except:
        print("Error converting to dataframe. Check XML")
        df=None
    return(df)

def getXMLFiles():
    soup = BeautifulSoup(requests.get(pageURL).text, "lxml")
    xmlTag = soup.find("div", class_="span-39 last")
    xmlLinks = xmlTag.find_all("a")
    xmlList = []
    for link in xmlLinks:
        try:
            xmlRequest = requests.get(xmlStub + link["href"])
            # Check to see if properly formated xml
            # There mus be a better way?
            root = ET.fromstring(xmlRequest.text)
            yield xmlRequest.text
        except: 
            print("Error on file: " + link.text)
    

if __name__ == "__main__":
    if(len(sys.argv) > 1):
        path = sys.argv[1]
    else:
        path = os.getcwd()
    print("Downloading XML Files....")
    xmlList = getXMLFiles()
    df = pd.concat(map(extractDataFrameFromXML, xmlList))
    print("Saving to " + path)
    feather.write_dataframe(df, path + "/NYTrafficData.feather")
    



