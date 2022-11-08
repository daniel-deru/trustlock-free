import sys
import os
import time
import keyboard
from threading import Thread
from pynput.mouse import Listener, Button

from PyQt5.QtCore import QObject, pyqtSignal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


class AutoType(QObject):
    finished: pyqtSignal = pyqtSignal(bool)
    previous_left: int = 0
    
    def __init__(self, things_to_type):
        super(AutoType, self).__init__()
        self.things_to_type = things_to_type
    
    def auto_type(self):
        for thing in self.things_to_type:
            with Listener(on_click=lambda x, y, b, p: self.on_click(b, p, thing)) as self.listener:
                Thread(target=self.time_out).start()
                self.listener.join()
        self.finished.emit(True)
                
    def on_click(self, button, pressed, thing):
        
        if button == Button.left and pressed:
            current_left = time.time()
            
            diff_time = current_left - self.previous_left
            self.previous_left = current_left
            if diff_time < 0.3:
                time.sleep(1)
                keyboard.write(text=thing, delay=0.005)
            
                self.listener.stop()
            
    def time_out(self, duration=20):
        time.sleep(duration)
        self.listener.stop()