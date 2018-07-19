'''
Created on 18 juil. 2018

@author: NathanKun
'''

import datetime

def log(logStr: str):
    timeStr = '{0:%Y-%m-%d_%H:%M:%S.%f}'.format(datetime.datetime.now())[:-3] + ": "
    logStr = timeStr + logStr
    print(logStr)
