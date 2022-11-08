import sys
import os

from PyQt5.QtCore import QObject, pyqtSignal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from integrations.calendar.c import Google

class GoogleDownload(QObject):
    finished: pyqtSignal = pyqtSignal(str)
    def download(self):
        name: str = Google.download_backup()
        self.finished.emit(name)
        
class GoogleUpload(QObject):
    finished: pyqtSignal = pyqtSignal(bool)
    def upload(self):
        Google.upload_backup()
        self.finished.emit(True)
        
        