from bs4 import BeautifulSoup
import urllib.request

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
            dt = next(tds[0].strings).string.replace("\n", "").replace("\t", "")
            
            # td2a has 2 case: with or without FanSub Group name => len = 1 or len = 2
            td2a = tds[2].find_all("a")
            if len(td2a) == 1:
                group = ""
                title = "".join(td2a[0].strings).replace("\n", "").replace("\t", "")
            else:
                group = td2a[0].string.replace("\n", "").replace("\t", "")
                title = "".join(td2a[1].strings).replace("\n", "").replace("\t", "")
            
            if titleMustContains not in title:
                continue
                
            uri = tds[3].find("a")["href"]
            size = tds[4].string
            print(dt)
            print(group)
            print(title)
            print(uri)
            print(size)

def main():
    print("-----------OVERLORD-----------")
    crawl("https://share.dmhy.org/topics/list?keyword=overlord+III+1080", "YMDR")
    print("-----------后街女孩-----------")
    crawl("https://share.dmhy.org/topics/list?keyword=%E5%90%8E%E8%A1%97%E5%A5%B3%E5%AD%A9+1080", "咪梦动漫组")
    print("-----------千緒的通學路-----------")
    crawl("https://share.dmhy.org/topics/list?keyword=%E5%8D%83%E7%BB%AA%E7%9A%84%E9%80%9A%E5%AD%A6%E8%B7%AF+1080", "极影字幕社", "GB")
    print("-----------殺戮天使-----------")
    crawl("https://share.dmhy.org/topics/list?keyword=angel+of+death+1080", "YMDR")
    print("-----------天狼-----------")
    crawl("https://share.dmhy.org/topics/list?keyword=%E5%A4%A9%E7%8B%BC+1080", "YMDR")
    

if __name__ == "__main__":
    main()
    
