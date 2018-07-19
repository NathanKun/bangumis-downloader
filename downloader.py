'''
Created on 19 juil. 2018

@author: jhe
'''
from util import baidunetdisk

TASK_NEW = "TASK_NEW"
TASK_TORRENT_DOWNLOADED = "TASK_TORRENT_DOWNLOADED"
TASK_BAIDU_CREATED = "TASK_BAIDU_CREATED"
TASK_BAIDU_DOWNLOADED = "TASK_BAIDU_DOWNLOADED"
TASK_DOWNLOADING = "TASK_DOWNLOADING"
TASK_DOWANLOADED = "TASK_DOWANLOADED"
TASK_ERROR = "TASK_ERROR"


def writeTasks(t):
    with open("tasks.json", "w+", encoding='utf8') as f:
        jsonStr = json.dumps(t, ensure_ascii=False)
        f.write(jsonStr)
    
    
def readTasks():
    with open("tasks.json", "r", encoding='utf8') as f:
        fStr = f.read()

    if fStr != "":
        log("tasks.json found")
        t = json.loads(fStr)
        return t
    else:
        log("tasks.json not found, will create one")
        return {}
        

def downloadTorrent(url, file_name):
    # Download the file from `url` and save it locally under `file_name`:
    with urllib.request.urlopen(url) as response, open("torrent/" + file_name, 'wb') as out_file:
        data = response.read() # a `bytes` object
        out_file.write(data)


def main():
    log("Downloader started")
    
    # read tasks file
    tasks = readTasks()
    
    
    # get online json
    log("Requesting bangumi list")
    f = urllib.request.urlopen("https://catprogrammer.com/bmu/bmu.json")  # request
    bangumis = Bangumi.jsonToList(f.read().decode("utf-8"))
    
    
    # update tasks
    for b in bangumis:
        found = False

        if b.title in tasks:
            found = True
            log("Exist " + b.title)
        
        if not found:
            tasks[b.title] = {"status": TASK_NEW, "bangumi": b.toJson()}
            log("New " + b.title)


    # save tasks file
    writeTasks(tasks)
    
    
    # check if all downloaded
    allDownloaded = True
    for _, value in tasks.items():
        if value["status"] != TASK_DOWANLOADED:
            allDownloaded = False
    if allDownloaded:
        log("All bangumis have been downloaded, stopping...")
        return
        
        
    # login baidu net disk
    log("Logging in to baidu net disk")
    if not netdisk.login():
        log("Can't handle that yet, stopping...")
        return
    log("Login OK")
    
    
    # handle TASK_NEW
    log("Handling TASK_NEW...")
    if not os.path.exists("torrent"):
        os.mkdir("torrent")
    for title, value in tasks.items():
        if value["status"] == TASK_NEW:
            log(title + " is TASK_NEW, downloading torrent...")
            
            torrentUrl = value["bangumi"]["torrentUrl"]
            urlSplited = torrentUrl.split("/")
            torrentFileName = urlSplited[len(urlSplited) - 1]
            downloadTorrent(torrentUrl, torrentFileName)
            
            tasks[title]["status"] = TASK_TORRENT_DOWNLOADED
            tasks[title]["torrentFileName"] = torrentFileName
            writeTasks(tasks)
            
            log(title + " torrent downloaded: " + torrentFileName)
        
        
    # handle TASK_TORRENT_DOWNLOADED
    log("Handling TASK_TORRENT_DOWNLOADED...")
    for title, value in tasks.items():
        if value["status"] == TASK_TORRENT_DOWNLOADED:
            log(title + " is TASK_TORRENT_DOWNLOADED, creating baidu task...")
            
            torrentFileName = value["torrentFileName"]
            baiduSavePath = "/bmu/" + title
            
            if not baidunetdisk.createBaiduTask("torrent/" + torrentFileName, baiduSavePath):
                log(title + " createBaiduTask failed")
            
            
            tasks[title]["status"] = TASK_BAIDU_CREATED
            tasks[title]["baiduSavePath"] = baiduSavePath
            writeTasks(tasks)
            
            log(title + " baidu task created")


    log("Finished, stopping...")


def except_hook(exctype, value, traceback):
    import traceback as tb
    log("Exception", withTime = False)
    log("exctype:", withTime = False)
    log(str(exctype), withTime = False)
    log("value:", withTime = False)
    log(str(value), withTime = False)
    log("traceback:", withTime = False)
    tbList = tb.format_tb(traceback, 100)
    for i in tbList:
        log(i, withTime = False) # limit = 100
        
    sys.__excepthook__(exctype, value, traceback)


if __name__ == "__main__":
    import sys
    sys.excepthook = except_hook
    
    import os, json
    import urllib.request
    from model.bangumi import Bangumi
    from util.logger import log
    import util.baidunetdisk as netdisk
    
    main()
