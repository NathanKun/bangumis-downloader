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
    
def crawl(url, groupName, titleMustContains=""):
    f = urllib.request.urlopen(url)
    soup = BeautifulSoup(f.read().decode("utf-8"), "lxml")
    
    table = soup.find_all(id="topic_list")
    if(len(table) != 1):
        raise Exception("Cannot find result table: len(table) = " + len(table))
    table = table[0]
    
    trs = table.find("tbody").find_all("tr")
    if(len(trs) == 0):
        raise Exception("No result: len(trs) == 0")
    
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

def main():
    rows = []
    rows.append(crawl("https://share.dmhy.org/topics/list?keyword=overlord+III+1080", "YMDR"))
    rows.append(crawl("https://share.dmhy.org/topics/list?keyword=%E5%90%8E%E8%A1%97%E5%A5%B3%E5%AD%A9+1080", "咪梦动漫组"))
    rows.append(crawl("https://share.dmhy.org/topics/list?keyword=%E5%8D%83%E7%BB%AA%E7%9A%84%E9%80%9A%E5%AD%A6%E8%B7%AF+1080", "极影字幕社", "GB"))
    rows.append(crawl("https://share.dmhy.org/topics/list?keyword=angel+of+death+1080", "YMDR"))
    rows.append(crawl("https://share.dmhy.org/topics/list?keyword=%E5%A4%A9%E7%8B%BC+1080", "YMDR"))
    
    htmlRows = ""
    for r in rows:
        htmlRows = htmlRows + r.toHtmlTableRow()
        
    print ('''
            <!doctype html>
            <html lang="en">
            
            <head>
              <meta charset="utf-8">
              <meta http-equiv="x-ua-compatible" content="ie=edge">
              <meta name="viewport" content="width=device-width, initial-scale=1">
            
              <title>Bangumis Magnet Uri</title>
            
              <link rel="stylesheet" href="css/main.css">
              <link rel="icon" href="images/favicon.png">
            </head>
            
            <body>
                <table>
                    <thead></thead>
                    <tbody>
            ''' + 
            htmlRows + 
            '''
                    </tbody>
                </table>
            </body>
            </html>
            ''')

if __name__ == "__main__":
    from bs4 import BeautifulSoup
    import urllib.request
    
    main()
    
