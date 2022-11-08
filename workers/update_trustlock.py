import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import requests
import json
import urllib3

from utils.globals import VERSION, PATH
from utils.message import Message

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal


class UpdateTrustLockWorker(QObject):
    finished = pyqtSignal(bool)
    progress = pyqtSignal(int)
    downloading = pyqtSignal(bool)
    requested = pyqtSignal(bool)
    error = pyqtSignal(bool)
    
    def __init__(self) -> None:
        super(UpdateTrustLockWorker, self).__init__()
        
        
    def download(self):
        url = "https://api.smartmetatec.com/index.php/update/download"
        r = None
        
        try:
            r = requests.post(url, stream=True, json={"email": "daniel@email.com"})
        except Exception:
           return self.error.emit(True)
            
        self.requested.emit(True)
        total_bytes = int(r.headers['Content-Length'])

        minimum_application_size = 50 * 1000 * 1000
        
        if(minimum_application_size > total_bytes):
            return
        
        save_path = PATH + "\\update.zip"
        
        with open(save_path, 'wb') as fd:
            current = 0
            self.downloading.emit(True)
            for chunk in r.iter_content(chunk_size=128):
                self.progress.emit(round((current/total_bytes) * 100))
                current += 128
                fd.write(chunk)
                
        self.finished.emit(True)

                
    def start(self):
        self.download()
