'''
Created on 18 juil. 2018

@author: NathanKun
'''

import datetime

def bangumiToHtmlTableRow(bangumi):
    return '''<tr>
            <td>{0}</td>
            <td>{1}</td>
            <td><a href='{2}'>{3}</a></td>
            <td><a href='{4}'>magnet uri</a></td>
            <td><a href='{5}'>torrent</a></td>
            <td>{6}</td>
            <td><a href='{7}'>Search</a></td>
            </tr>'''.format(bangumi.uploadedAt,
                            bangumi.group,
                            bangumi.postUrl,
                            bangumi.title,
                            bangumi.magnetUri,
                            bangumi.torrentUrl,
                            bangumi.size,
                            bangumi.searchUrl)

def combineRowsToTable(bangumiName, htmlRows):
    return '''
            <h4>{0}</h4>
            <table class="zui-table">
                <thead><tr>
                    <th>上传时间⏰</th>
                    <th>字幕组</th>
                    <th>标题📃</th>
                    <th>磁链</th>
                    <th>种子</th>
                    <th>大小</th>
                    <th>搜索🔍</th>
                </tr></thead>
                <tbody>
                    {1}
                </tbody>
            </table>'''.format(bangumiName, htmlRows)
    
def generateResultPage(htmlTables):
    return '''
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
                      margin-bottom: 5vh;
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
                {1}
            </body>
            </html>
            '''.format('{0:%Y-%m-%d_%H:%M:%S}'.format(datetime.datetime.now()), htmlTables)