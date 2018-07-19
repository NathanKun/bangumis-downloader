'''
Created on 19 juil. 2018

@author: NathanKun
'''

import json
from requests import Response
from baidupcsapi import PCS
from model import const
from util.logger import log


pcs = None


def login(captcha_callback=None, verify_callback=None):
    """
    :param captcha_callback: 验证码的回调函数
        .. note::
            该函数会获得一个jpeg文件的内容，返回值需为验证码
    :param verify_callback: 安全验证码输入函数
        .. note::
            该函数返回值为字符串作为安全验证码输入
    """
    
    global pcs
    pcs = PCS(const.username, const.password, 
              captcha_callback=captcha_callback, verify_callback=verify_callback)
    
    response = pcs.quota()
    
    if not isinstance(response, Response):
        log("Request error")
        return False
        
    response = response.content.decode('utf-8')
    
    if json.loads(response)["errno"] != 0:
        log("Response error")
        log("pcs.quota() returns:")
        log(response)
        return False
    
    return True

def createBaiduTask(torrent_path, save_path):
    """
                添加本地BT任务
    :param torrent_path: 本地种子的路径
    :param save_path: 远程保存路径
            返回正确时返回的 Reponse 对象 content 中的数据结构
            {"task_id":任务编号,"rapid_download":是否已经完成（急速下载）,"request_id":请求识别号}
    """
    
    global pcs
    response = pcs.add_torrent_task(torrent_path, save_path)
    
    if not isinstance(response, Response):
        log("Request error")
        return False
    
    response = json.loads(response.content.decode('utf-8'))
    log(response)
    
    return True
