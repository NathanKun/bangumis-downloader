# Bangumis Auto Downloader
A script for downloading your following bangumis automatically.

## How to
### Config
Update the array 'target' in bmu.py  
Example:  
```python
targets = [{
            "name": "骨傲天3",
            "url": "https://share.dmhy.org/topics/list?keyword=overlord+III+1080",
            "group": "YMDR"
        }, {
            "name": "后街女孩",
            "url": "https://share.dmhy.org/topics/list?keyword=%E5%90%8E%E8%A1%97%E5%A5%B3%E5%AD%A9+1080",
            "group": "咪梦动漫组"
        }]
```

#### Parameters explication:  
<b>name</b>: Required. Name of the folder of the bangumi  

<b>url</b>: Required. Search url of dmhy.org.  

<b>group</b>: Required. Subfans group name for filtering search result.  

<b>keyword</b>: Optional. A keyword for filtering search result, , in case a subfans group release multiples versions for a same episode, for example GB and BIG5.  

### Run
Run `python3 downloader.py -p path_to_save_torrents_and_bangumis` to start downloading  
beautifulsoup4 is required  

### Download
A torrent folder will be created in the given path, for saving torrents of bangumis.  
For each target, a folder with the given name will be created, all episodes of this bangumi will be saved in this folder.  
A task.json will be created in the project folder, for saving episodes downloaded.  

### Automation
You can use unix crontab / windows task scheduler to run the script automatically multiple times per days.  Once a new episode is released, the downloader will find it and download it automatically.  
