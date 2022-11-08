import sys
import os
import pyperclip

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from utils.helpers import set_font

class RegisterWordButton(QPushButton): 
    
    def __init__(self, data, number=None):
        super(RegisterWordButton, self).__init__()
        self.data = data
        self.clicked.connect(lambda: pyperclip.copy(data))

        set_font([self])
        
        self.setCursor(Qt.PointingHandCursor)
        self.setText(f"{str(number).zfill(2)}. {data}")
        self.setStyleSheet("""QPushButton {
                                text-align: left;
                                background-color: white;
                                border: 2px solid #9ecd16;
                                color: black;
                            }
                            QPushButton:hover {
                                background-color: #9ecd16;
                                color: white;
                            }
                            QPushButton:pressed {
                                    background-color: white;
                                    color: black;
                            }""")
        
        
    
        
        
        