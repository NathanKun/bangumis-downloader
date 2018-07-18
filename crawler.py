'''
Created on 18 juil. 2018

@author: NathanKun
'''

import urllib.request
from bs4 import BeautifulSoup
from logger import log
from bangumi import Bangumi

def crawl(url: str, groupName: str, titleMustContains = ""):
    episodes = [] # to return all found Bangumi objects
    f = urllib.request.urlopen(url) # request
    soup = BeautifulSoup(f.read().decode("utf-8"), "lxml") # bs4
    
    table = soup.find_all(id="topic_list") # <table> which contains all search results
    if(len(table) != 1):
        raise Exception("Cannot find result table: len(table) = " + len(table))
    table = table[0]
    
    trs = table.find("tbody").find_all("tr") # get all table rows
    if(len(trs) == 0):
        #raise Exception("No result: len(trs) == 0")
        log("No result for url = " + url)
    
    # foreach row
    for tr in trs:
        strs = tr.strings
        found = False
        
        # check if the specified fansub group name is in this row
        for s in strs:
            if groupName in s:
                found = True
                break
        
        # if the fansub group name is in this row, extract all info needed to create a Banguli object, and add to array
        if found:
            tds = tr.find_all("td")
            uploadedAt = next(tds[0].strings).string.replace("\n", "").replace("\t", "")
            
            # td2a has 2 case: with or without FanSub Group name => len = 1 or len = 2
            td2a = tds[2].find_all("a")
            if len(td2a) == 1:
                group = ""
                title = "".join(td2a[0].strings).replace("\n", "").replace("\t", "")
                postUrl = td2a[0]["href"]
            else:
                group = td2a[0].string.replace("\n", "").replace("\t", "")
                title = "".join(td2a[1].strings).replace("\n", "").replace("\t", "")
                postUrl = td2a[1]["href"]
            
            if titleMustContains not in title:
                continue
                
            postUrl = "https://share.dmhy.org" + postUrl
            magnetUri = tds[3].find("a")["href"]
            size = tds[4].string
            
            episodes.append(Bangumi(uploadedAt, group, title, magnetUri, size, postUrl, url))
        # if found: END
    # for tr in trs:
    return episodes
