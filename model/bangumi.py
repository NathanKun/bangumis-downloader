'''
Created on 18 juil. 2018

@author: NathanKun
'''


import json
from json import JSONEncoder, JSONDecoder


class Bangumi:
    def __init__(self, uploadedAt: str, group: str, title: str, magnetUri: str,
                 size: str, postUrl: str, searchUrl: str, torrentUrl: str):
        self.uploadedAt = uploadedAt
        self.group = group
        self.title = title
        self.magnetUri = magnetUri
        self.size = size
        self.postUrl = postUrl
        self.searchUrl = searchUrl
        self.torrentUrl = torrentUrl
        
    def toJson(self):
        return self.__dict__
    
    @staticmethod
    def fromJson(jsonStr):
        BangumiDecoder.decode(jsonStr)

    @staticmethod
    def listToJson(bangumis):
        return json.dumps(bangumis, cls=BangumiEncoder)
    
    @staticmethod
    def jsonToList(jsonStr):
        return BangumiDecoder.decode(jsonStr)


class BangumiEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__  
        
        
class BangumiDecoder():
    @staticmethod
    def from_json(jsonStr):
        uploadedAt = jsonStr["uploadedAt"] if 'uploadedAt' in jsonStr else ""
        group = jsonStr["group"] if 'group' in jsonStr else ""
        title = jsonStr["title"] if 'title' in jsonStr else ""
        magnetUri = jsonStr["magnetUri"] if 'magnetUri' in jsonStr else ""
        size = jsonStr["size"] if 'size' in jsonStr else ""
        postUrl = jsonStr["postUrl"] if 'postUrl' in jsonStr else ""
        searchUrl = jsonStr["searchUrl"] if 'searchUrl' in jsonStr else ""
        torrentUrl = jsonStr["torrentUrl"] if 'torrentUrl' in jsonStr else ""
        
        return Bangumi(uploadedAt, group, title, magnetUri, size, postUrl, searchUrl, torrentUrl)
    
    @staticmethod
    def decode(json: str):
        return JSONDecoder(object_hook = BangumiDecoder.from_json).decode(json)
