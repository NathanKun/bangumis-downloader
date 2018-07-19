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

    @staticmethod
    def listToJson(bangumis):
        return json.dumps(bangumis, cls=BangumiEncoder)
    
    @staticmethod
    def jsonToList(json):
        BangumiDecoder.decode(json)


class BangumiEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__  
        
        
class BangumiDecoder():
    @staticmethod
    def from_json(json):
        uploadedAt = ""
        group = ""
        title = ""
        magnetUri = ""
        size = ""
        postUrl = ""
        searchUrl = ""
        torrentUrl = ""
        
        if 'uploadedAt' in json:
            uploadedAt = json["uploadedAt"]
        if 'group' in json:
            group = json["group"]
        if 'title' in json:
            title = json["title"]
        if 'magnetUri' in json:
            magnetUri = json["magnetUri"]
        if 'size' in json:
            size = json["size"]
        if 'postUrl' in json:
            postUrl = json["postUrl"]
        if 'searchUrl' in json:
            searchUrl = json["searchUrl"]
        if 'torrentUrl' in json:
            torrentUrl = json["torrentUrl"]
        
        return Bangumi(uploadedAt, group, title, magnetUri, size, postUrl, searchUrl, torrentUrl)
    
    @staticmethod
    def decode(json: str):
        return JSONDecoder(object_hook = BangumiDecoder.from_json).decode(json)
