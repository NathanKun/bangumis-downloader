'''
Created on 18 juil. 2018

@author: NathanKun
'''

import htmlhelper

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
        
    def toHtmlTableRow(self):
        return htmlhelper.bangumiToHtmlTableRow(self)
    