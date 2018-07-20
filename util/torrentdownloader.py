'''
Created on 20 juil. 2018

@author: NathanKun
'''

import sys, time
import libtorrent as lt

class TorrentDownloader:
    
    def __init__(self):
        self.ses = lt.session()
        self.ses.listen_on(6881, 6891)
    
    def download(self, torrentPath, savePath):
        info = lt.torrent_info(torrentPath)
        h = self.ses.add_torrent({'ti': info, 'save_path': savePath})
        print('starting', h.name())
        
        while (not h.is_seed()):
            s = h.status()
            
            state_str = ['queued', 'checking', 'downloading metadata', \
                         'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']
            print('\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
                (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
                s.num_peers, state_str[s.state]),)
            sys.stdout.flush()
            
            time.sleep(1)
        
        print(h.name(), 'complete')
      
