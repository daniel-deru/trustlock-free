import sys
import os

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from utils.message import Message

class UpdatePasswordWorker(QObject):
    finished: pyqtSignal = pyqtSignal(bool)
    
    def __init__(self) -> None:
        super(UpdatePasswordWorker, self).__init__()
        
    def ask(self):
        response = Message("There are some password that have expired. Do you want to update them?", "Expired Passwords").prompt()
        # store bool based on user input yes = True no = False
        response = response == QMessageBox.Yes
        self.finished.emit(response)