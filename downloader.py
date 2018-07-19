'''
Created on 19 juil. 2018

@author: jhe
'''

TASK_NEW = "TASK_NEW"
TASK_LIXIAN_CREATED = "TASK_LIXIAN_CREATED"
TASK_LIXIAN_DOWNLOADED = "TASK_LIXIAN_DOWNLOADED"
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
    pcs = PCS(const.username, const.password)
    quota = pcs.quota().content.decode('utf-8')
    if json.loads(quota)["errno"] != 0:
        log("Error")
        log("pcs.quota() returns:")
        log(quota)
        log("Can't handle that yet, stopping...")
        return

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
    
    import urllib.request
    import json
    from baidupcsapi import PCS
    from model.bangumi import Bangumi
    from util.logger import log
    from model import const
    
    main()
