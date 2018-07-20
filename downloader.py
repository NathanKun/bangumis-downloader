"""
Bangumis Magnet Uri
Crawl share.dmhy.org to get the magnet uris of my following bangumis.
Find all episodes not downloaded, download its torrents, then download the bangumis.
"""

__author__ = "NathanKun"
__version__ = "1.0"
__maintainer = "NathanKun,"



TASK_NEW = "TASK_NEW"
TASK_TORRENT_DOWNLOADED = "TASK_TORRENT_DOWNLOADED"
TASK_BAIDU_CREATED = "TASK_BAIDU_CREATED"
TASK_BAIDU_DOWNLOADED = "TASK_BAIDU_DOWNLOADED"
TASK_DOWNLOADING = "TASK_DOWNLOADING"
TASK_DOWNLOADED = "TASK_DOWNLOADED"
TASK_ERROR = "TASK_ERROR"



def handleInput(argv):
    savePath = ''
    opts, _ = getopt.getopt(argv, "hp:")
    for opt, arg in opts:
        if opt == "-h":
            print("downloader.py [option]")
            print(' -h Help')
            print(' -p Path to save bangumis, required')
            return False, ""
        elif opt == "-p":
            savePath = arg
            if not pathutil.is_path_exists_or_creatable(savePath):
                log("Path not valid")
                return False, ""
            log("Path to save bangumis: " + savePath)
    
    if savePath == '':
        log("No path in input, use -p PATH to specify a folderto save bangumis.")
        return False, ""
    
    return True, savePath


def writeTasks(t):
    with open("tasks.json", "w+", encoding='utf8') as f:
        jsonStr = json.dumps(t, indent=4, ensure_ascii=False)
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
        

def downloadTorrent(url, file_name, savePathTorrent):
    # Download the file from `url` and save it locally under `file_name`:
    with urllib.request.urlopen(url) as response, open(savePathTorrent + file_name, 'wb') as out_file:
        data = response.read() # a `bytes` object
        out_file.write(data)


def main(argv):
    
    # handle inputs
    try:
        inputResult, savePath = handleInput(argv)
        if not inputResult:
            return
    except getopt.GetoptError as e:
        log("Error: " + e.msg)
        return
    
    
    log("Downloader started")
    
    savePathTorrent = savePath + "/torrent/"
    if not os.path.exists(savePath):
        os.mkdir(savePath)
    if not os.path.exists(savePathTorrent):
        os.mkdir(savePathTorrent)
    
    
    # read tasks file
    try:
        tasks = readTasks()
    except: # file not exists
        tasks = {}
    
    '''
    # get online json
    log("Requesting bangumi list")
    f = urllib.request.urlopen("https://catprogrammer.com/bmu/bmu.json")  # request
    bangumis = Bangumi.jsonToList(f.read().decode("utf-8"))
    '''
    
    # Crawl targets
    log("Requesting bangumi list...")
    _, bangumis = crawlTargets(targets)
    bangumis = Bangumi.jsonToList(bangumis)
    
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
        if value["status"] != TASK_DOWNLOADED:
            allDownloaded = False
    if allDownloaded:
        log("All bangumis have been downloaded, stopping...")
        return
        
    '''
    # login baidu net disk
    log("Logging in to baidu net disk")
    if not netdisk.login():
        log("Can't handle that yet, stopping...")
        return
    log("Login OK")
    '''
    
    # handle TASK_NEW
    log("Handling TASK_NEW...")
    for title, value in tasks.items():
        if value["status"] == TASK_NEW:
            log(title + " is TASK_NEW, downloading torrent...")
            
            torrentUrl = value["bangumi"]["torrentUrl"]
            urlSplited = torrentUrl.split("/")
            torrentFileName = urlSplited[len(urlSplited) - 1]
            downloadTorrent(torrentUrl, torrentFileName, savePathTorrent)
            
            tasks[title]["status"] = TASK_TORRENT_DOWNLOADED
            tasks[title]["torrentFileName"] = torrentFileName
            writeTasks(tasks)
            
            log(title + " torrent downloaded: " + torrentFileName)
        
        
    # handle TASK_TORRENT_DOWNLOADED
    log("Handling TASK_TORRENT_DOWNLOADED...")
    td = TorrentDownloader()
    for title, value in tasks.items():
        if value["status"] == TASK_TORRENT_DOWNLOADED:
            '''
            log(title + " is TASK_TORRENT_DOWNLOADED, creating baidu task...")
            
            torrentFileName = value["torrentFileName"]
            baiduSavePath = "/bmu/" + title
            
            if not baidunetdisk.createBaiduTask("torrent/" + torrentFileName, baiduSavePath):
                log(title + " createBaiduTask failed")
            
            
            tasks[title]["status"] = TASK_BAIDU_CREATED
            tasks[title]["baiduSavePath"] = baiduSavePath
            writeTasks(tasks)
            
            log(title + " baidu task created")
            '''
            torrentPath = "torrent/" + value["torrentFileName"]
            savePathBangumi = savePath + "/" + value["bangumi"]["name"]
            
            log("Downloading " + title)
            tasks[title]["status"] = TASK_DOWNLOADING
            writeTasks(tasks)
            
            td.download(torrentPath, savePathBangumi)
            
            log("Downloaded " + title)
            tasks[title]["status"] = TASK_DOWNLOADED
            writeTasks(tasks)
            

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
    
    import os, getopt, json
    import urllib.request
    from util.logger import log
    from util.torrentdownloader import TorrentDownloader
    from util.crawler import crawlTargets
    from util import pathutil
    from bmu import targets
    from model.bangumi import Bangumi
    #import util.baidunetdisk as netdisk
    
    main(sys.argv[1:])
