# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 11:19:31 2016

@author: Dillon R. Gardner
"""

import requests
import pandas as pd
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

pageStart = requests.get("http://web.mta.info/developers/data/bandt/trafficdata.html")
soup = BeautifulSoup(pageStart.text)
xmlStub = "http://web.mta.info/developers/data/bandt/"

tmp = soup.find_all("div", class_="span-39 last")[0].find_all("a")[0]["href"]
xmlFile = requests.get(xmlStub + tmp)

root = ET.fromstring(xmlFile.text)

for d in root:
    print(d.attrib)
    for child in d:
        print(pd.DataFrame(child.attrib))
        
 def dictionariesFromDay(day):
     dictionaries = []
     for child in day:
         newDict = child.attrib
         newDict.update(day.attrib)
         dictionaries.append(newDict)
     return(dictionaries)
       
dictionaries = []
for day in root:
    newDicts = dictionariesFromDay(day) for day in root]
    dictionaries.append(newDict)
tmp = pd.DataFrame(dictionaries)



[i for i in range(5)]

def fetchactor(gender, cat, limit = None):
    if gender.lower() == 'male':
        rest = 'male_'+cat.lower()+'_actors'
    else: rest = str(cat).lower()+'_actresses'
    pagestart = urllib2.urlopen(wikisource+'/w/index.php?title=Category:American_'+rest+'&from=A')
                                                             
    pagestart = pagestart.read()
    soup = BeautifulSoup(pagestart)
    actor = []
    i = 0
    if limit == None: lim = float('inf')
    else: lim = limit

    while i < lim:
        div = soup.find('div', id = 'mw-pages')
        for namelist in div.find_all('ul'):
            for name in namelist.find_all('a'):
                if name != []: actor.append(name.contents[0])
        nextpage = div.find('a',text = 'next 200')
        if nextpage != None:
            filmnext = urllib2.urlopen(wikisource+nextpage['href'])
            filmnext = filmnext.read()
            soup = BeautifulSoup(filmnext)
        else: break
        i += 200
    return actor
    
    http://web.mta.info/developers/data/bandt/tbta_plaza/PLAZA_DAILY_TRAFFIC_20160912.xml