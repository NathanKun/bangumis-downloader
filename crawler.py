'''
Created on 18 juil. 2018

@author: NathanKun
'''

import urllib.request
from bs4 import BeautifulSoup
from threading import Thread
from logger import log
from bangumi import Bangumi
import htmlhelper


def crawlPostPage(episode: Bangumi, parentThreadIndex, index):
    log("Thread {0}.{1} started".format(parentThreadIndex, index))
    f = urllib.request.urlopen(episode.postUrl)  # request
    soup = BeautifulSoup(f.read().decode("utf-8"), "lxml")  # bs4
    
    torrentUrl = soup.find(id="tabs-1").find_all("p")[0].find_all("a")[0]["href"]
    
    if torrentUrl.endswith(".torrent"):
        if torrentUrl.startswith("//"):
            torrentUrl = "https:" + torrentUrl
    else:
        torrentUrl = "error"
        
    episode.torrentUrl = torrentUrl
    
    print(torrentUrl)
    log("Thread {0}.{1} stopped".format(parentThreadIndex, index))
    
    
def crawlSearchPage(url: str, groupName: str, threadIndex, titleMustContains=""):
    episodes = []  # to return all found Bangumi objects
    f = urllib.request.urlopen(url)  # request
    soup = BeautifulSoup(f.read().decode("utf-8"), "lxml")  # bs4
    
    table = soup.find_all(id="topic_list")  # <table> which contains all search results
    if(len(table) != 1):
        raise Exception("Cannot find result table: len(table) = " + len(table))
    table = table[0]
    
    trs = table.find("tbody").find_all("tr")  # get all table rows
    if(len(trs) == 0):
        # raise Exception("No result: len(trs) == 0")
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
            
            episodes.append(Bangumi(uploadedAt, group, title, magnetUri, size, postUrl, url, ""))
        # if found: END
    # for tr in trs:
    
    if len(episodes) == 0:
        return episodes
    
    # crawl post page for all episodes to get torrent url
    threads = [None] * len(episodes)
    
    # start a thread for each episodes
    for i in range(len(episodes)):
        threads[i] = Thread(target=crawlPostPage, args=(episodes[i], threadIndex, i))
        threads[i].start()
    
    # wait all threads to finish
    for i in range(len(episodes)):
        threads[i].join()
    
    return episodes
    

def crawlTargets(targets):
    htmlTablesArray = [None] * len(targets)
    threads = [None] * len(targets)
    
    # crawlSearchPage one target function, save the result to "htmlTablesArray" object
    def crawlOneTarget(results, index, target):
        log("Thread {0} started".format(index))
        if("keyword" in target):
            episodes = crawlSearchPage(target["url"], target["group"], index, target["keyword"])
        else:
            episodes = crawlSearchPage(target["url"], target["group"], index)
                              
        if len(episodes) == 0:
            log("Thread {0} stopped, no episode found".format(index))
            return
        
        htmlRows = ""
        for e in episodes:
            htmlRows = htmlRows + htmlhelper.bangumiToHtmlTableRow(e)
            
        htmlTable = htmlhelper.combineRowsToTable(target["name"], htmlRows)
        results[index] = htmlTable
        log("Thread {0} stopped, found {1} episode(s)".format(index, len(episodes)))
    
    # start a thread for each target
    for i in range(len(targets)):
        threads[i] = Thread(target=crawlOneTarget, args=(htmlTablesArray, i, targets[i]))
        threads[i].start()
    
    # wait all threads to finish
    for i in range(len(targets)):
        threads[i].join()
    
    # concat all tables
    htmlTables = ""
    for i in range(len(targets)):
        htmlTables = htmlTables + htmlTablesArray[i]
        
    
        
    return htmlTables