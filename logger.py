'''
Created on 18 juil. 2018

@author: NathanKun
'''

import os, datetime

logFilePath = "log/bmu_{0}.log".format("{0:%Y%m%d_%H%M%S}".format(datetime.datetime.now()))
if not os.path.exists("log"):
    os.mkdir("log")


def log(logStr: str, withTime=True):
    timeStr = ''
    if withTime:
        timeStr = '{0:%Y-%m-%d_%H:%M:%S.%f}'.format(datetime.datetime.now())[:-3] + ": "
    logStr = timeStr + logStr
    print(logStr)
    
    with open(logFilePath, "a", encoding='utf8') as f:
        f.write(logStr + "\n")
