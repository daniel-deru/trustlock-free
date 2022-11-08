import sys
import os
import time
import keyboard
from threading import Thread
import pyotp
from datetime import datetime

from PyQt5.QtCore import QObject, pyqtSignal

class TOTPCounter(QObject):
    time_signal = pyqtSignal(int)
    def __init__(self, code) -> None:
        super().__init__()
        self.code = code
        
    def count(self):
        while True:
            time.sleep(1)
            totp = pyotp.TOTP(self.code)
            time_left = totp.interval - datetime.now().timestamp() % totp.interval
            self.time_signal.emit(round(time_left))