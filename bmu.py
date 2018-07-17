"""
Bangumis Magnet Uri
Crawl share.dmhy.org to get the magnet uris of my following bangumis
"""

__author__ = "Junyang HE"
__version__ = "1.0"
__maintainer = "Junyang HE,"

class Bangumi:
    def __init__(self, uploadedAt, group, title, magnetUri, size, postUrl, searchUrl):
        self.uploadedAt = uploadedAt
        self.group = group
        self.title = title
        self.magnetUri = magnetUri
        self.size = size
        self.postUrl = postUrl
        self.searchUrl = searchUrl
        
    def toHtmlTableRow(self):
        return '''<tr>
                <td>{0}</td>
                <td>{1}</td>
                <td><a href='{2}'>{3}</a></td>
                <td><a href='{4}'>magnet uri</a></td>
                <td>{5}</td>
                <td><a href='{6}'>Search</a></td>
                </tr>'''.format(self.uploadedAt,
                                self.group,
                                self.postUrl,
                                self.title,
                                self.magnetUri,
                                self.size,
                                self.searchUrl)
    

def log(logStr):
    timeStr = '{0:%Y-%m-%d_%H:%M:%S.%f}'.format(datetime.datetime.now())[:-3] + ": "
    logStr = timeStr + logStr
    print(logStr)

def crawl(url, groupName, titleMustContains=""):
    f = urllib.request.urlopen(url)
    soup = BeautifulSoup(f.read().decode("utf-8"), "lxml")
    
    table = soup.find_all(id="topic_list")
    if(len(table) != 1):
        raise Exception("Cannot find result table: len(table) = " + len(table))
    table = table[0]
    
    trs = table.find("tbody").find_all("tr")
    if(len(trs) == 0):
        #raise Exception("No result: len(trs) == 0")
        log("No result for url = " + url)
    
    for tr in trs:
        strs = tr.strings
        found = False
        for s in strs:
            if groupName in s:
                found = True
                break
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
            
            return Bangumi(uploadedAt, group, title, magnetUri, size, postUrl, url)

def main(argv):
    
    # inputs
    htmlSaveToPath = ''
    opts, _ = getopt.getopt(argv, "hp:")
    for opt, arg in opts:
        if opt == "-h":
            print("BangumisMagnetUri.py [option]")
            print(' -h Help')
            print(' -p Path to save the html file generated, if not specified, will print to output directly')
            return
        elif opt == "-p":
            htmlSaveToPath = arg
            if not pathutil.is_path_exists_or_creatable(htmlSaveToPath):
                log("Path not valid")
                return
            log("Path to save the html file: " + htmlSaveToPath + "/bmu.html")
    
    if htmlSaveToPath == '':
        log("No path in input, use -p PATH to save the html file generated, or result will be print to output directly.")
    
    
    # targets to crawl
    targets = [{
                # 骨傲天3
                "url": "https://share.dmhy.org/topics/list?keyword=overlord+III+1080",
                "group": "YMDR"
            }, {
                # 后街女孩
                "url": "https://share.dmhy.org/topics/list?keyword=%E5%90%8E%E8%A1%97%E5%A5%B3%E5%AD%A9+1080",
                "group": "咪梦动漫组"
            }, {
                # 千绪的通学路
                "url": "https://share.dmhy.org/topics/list?keyword=%E5%8D%83%E7%BB%AA%E7%9A%84%E9%80%9A%E5%AD%A6%E8%B7%AF+1080",
                "group": "极影字幕社",
                "keyword": "GB"
            }, {
                # 杀戮天使
                "url": "https://share.dmhy.org/topics/list?keyword=angel+of+death+1080",
                "group": "YMDR"
            }, {
                # 天狼
                "url": "https://share.dmhy.org/topics/list?keyword=%E5%A4%A9%E7%8B%BC+1080", 
                "group": "YMDR"
            }]
    
    
    # Crawl
    log("Crawling...")
    
    rows = []
    for t in targets:
        if("keyword" in t):
            rows.append(crawl(t["url"], t["group"], t["keyword"]))
        else:
            rows.append(crawl(t["url"], t["group"]))
    
    
    # Generate result
    log("Generating result...")
    
    htmlRows = ""
    for r in rows:
        htmlRows = htmlRows + r.toHtmlTableRow()
        
    resultPage = '''
            <!doctype html>
            <html lang="zh-cmn">
            
            <head>
                <meta charset="utf-8">
                <meta http-equiv="x-ua-compatible" content="ie=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>Bangumis Magnet Uri</title>
                <style>
                .zui-table {{
                      border: solid 1px #DDEEEE;
                      border-collapse: collapse;
                      border-spacing: 0;
                      font: normal 13px Arial, sans-serif;
                  }}
                  .zui-table thead th {{
                      background-color: #DDEFEF;
                      border: solid 1px #DDEEEE;
                      color: #336B6B;
                      padding: 10px;
                      text-align: left;
                      text-shadow: 1px 1px 1px #fff;
                  }}
                  .zui-table tbody td {{
                      border: solid 1px #DDEEEE;
                      color: #333;
                      padding: 10px;
                      text-shadow: 1px 1px 1px #fff;
                  }}
                </style>
            </head>
            
            <body>
                <h3>Last Run At: {0}</h3>
                <table class="zui-table">
                    <thead><tr>
                        <th>上传时间⏰</th>
                        <th>字幕组</th>
                        <th>标题📃</th>
                        <th>磁链</th>
                        <th>大小</th>
                        <th>搜索🔍</th>
                    </tr></thead>
                    <tbody>
                        {1}
                    </tbody>
                </table>
            </body>
            </html>
            '''.format('{0:%Y-%m-%d_%H:%M:%S}'.format(datetime.datetime.now()), htmlRows)
    
    resultPage = BeautifulSoup(resultPage, "lxml").prettify()

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
    from bs4 import BeautifulSoup
    import urllib.request
    import datetime
    import os, sys, getopt
    import pathutil
    
    main(sys.argv[1:])
    
