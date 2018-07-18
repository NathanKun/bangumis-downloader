"""
Bangumis Magnet Uri
Crawl share.dmhy.org to get the magnet uris of my following bangumis
"""

__author__ = "Junyang HE"
__version__ = "1.0"
__maintainer = "Junyang HE,"


# targets to crawl
targets = [{
            "name": "骨傲天3",
            "url": "https://share.dmhy.org/topics/list?keyword=overlord+III+1080",
            "group": "YMDR"
        }, {
            "name": "后街女孩",
            "url": "https://share.dmhy.org/topics/list?keyword=%E5%90%8E%E8%A1%97%E5%A5%B3%E5%AD%A9+1080",
            "group": "咪梦动漫组"
        }, {
            "name": "千绪的通学路",
            "url": "https://share.dmhy.org/topics/list?keyword=%E5%8D%83%E7%BB%AA%E7%9A%84%E9%80%9A%E5%AD%A6%E8%B7%AF+1080",
            "group": "极影字幕社",
            "keyword": "GB"
        }, {
            "name": "杀戮天使",
            "url": "https://share.dmhy.org/topics/list?keyword=angel+of+death+1080",
            "group": "YMDR"
        }, {
            "name": "天狼",
            "url": "https://share.dmhy.org/topics/list?keyword=%E5%A4%A9%E7%8B%BC+1080", 
            "group": "YMDR"
        }]


def handleInput(argv):
    htmlSaveToPath = ''
    opts, _ = getopt.getopt(argv, "hp:")
    for opt, arg in opts:
        if opt == "-h":
            print("BangumisMagnetUri.py [option]")
            print(' -h Help')
            print(' -p Path to save the html file generated, if not specified, will print to output directly')
            return False, ""
        elif opt == "-p":
            htmlSaveToPath = arg
            if not pathutil.is_path_exists_or_creatable(htmlSaveToPath):
                log("Path not valid")
                return False, ""
            log("Path to save the html file: " + htmlSaveToPath + "/bmu.html")
    
    if htmlSaveToPath == '':
        log("No path in input, use -p PATH to save the html file generated, or result will be print to output directly.")
    
    return True, htmlSaveToPath


def crawlTargets():
    htmlTables = ""
    
    for t in targets:
        if("keyword" in t):
            episodes = crawl(t["url"], t["group"], t["keyword"])
        else:
            episodes = crawl(t["url"], t["group"])
                              
        if len(episodes) == 0:
            continue
        
        htmlRows = ""
        for e in episodes:
            htmlRows = htmlRows + e.toHtmlTableRow()
            
        htmlTable = htmlhelper.combineRowsToTable(t["name"], htmlRows)
                
        htmlTables = htmlTables + htmlTable
        
    return htmlTables

def main(argv):
    
    # handle inputs
    inputResult, htmlSaveToPath = handleInput(argv)
    if not inputResult:
        return
    
    
    # Crawl
    log("Crawling...")
    htmlTables = crawlTargets()
    
    
    # Generate result
    log("Generating result...")
    resultPage = htmlhelper.generateResultPage(htmlTables)
    resultPage = BeautifulSoup(resultPage, "lxml").prettify()


    # Output
    if htmlSaveToPath == '':
        log("Result Page:")
        print(resultPage)
    else:
        if not os.path.exists(htmlSaveToPath):
            os.mkdir(htmlSaveToPath)
            
        file = open(htmlSaveToPath + "/bmu.html", 'w+', encoding='utf8')
        file.write(resultPage)
        file.close()
        
    log("Finished")


if __name__ == "__main__":
    import os, sys, getopt
    from bs4 import BeautifulSoup
    import pathutil
    from logger import log
    from crawler import crawl
    import htmlhelper
    
    main(sys.argv[1:])
    
