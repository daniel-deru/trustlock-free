import sys
import os
import webbrowser

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCursor, QFont

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.PushButton import PushButtonLink

from utils.helpers import set_font, StyleSheet

from database.model import Model

class SetupWidget(QWidget):
    next_signal = pyqtSignal(bool)
    def __init__(self, data) -> None:
        super(SetupWidget, self).__init__()
        self.message = data[0]
        self.help_link = data[1]
        self.callback = data[2]
        self.step = data[3]
        self.create_ui()
        
        self.no_button.clicked.connect(lambda: self.next_signal.emit(True))
        self.yes_button.clicked.connect(self.run_callback)
        self.btn_help.clicked.connect(lambda: webbrowser.open_new_tab(self.help_link))
        
    def run_callback(self):
        self.callback()
        self.next_signal.emit(True)
        
    
    def create_ui(self):
        vbox = QVBoxLayout()
        
        hbox_button_container = QHBoxLayout()
        
        self.yes_button = QPushButton("Yes")
        self.yes_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.no_button = QPushButton("Skip")
        self.no_button.setCursor(QCursor(Qt.PointingHandCursor))
        
        hbox_button_container.addWidget(self.yes_button)
        hbox_button_container.addWidget(self.no_button)
        
        lbl_message: QLabel = QLabel(self.message)
        lbl_message.setAlignment(Qt.AlignCenter)
        lbl_message.setStyleSheet("font-size: 20px;font-weight: bold;")
        
        self.btn_help = QPushButton("What's This?")
        self.btn_help.setStyleSheet(StyleSheet([PushButtonLink()]).create())
        self.btn_help.setCursor(QCursor(Qt.PointingHandCursor))
        btn_container = QHBoxLayout()
        btn_container.addWidget(self.btn_help)
        
        vbox.addWidget(lbl_message)
        if self.help_link:
            vbox.addLayout(btn_container)
        vbox.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        vbox.addLayout(hbox_button_container)
        
        self.setLayout(vbox)
        
        font_list = [
            self.btn_help,
            self.no_button,
            self.yes_button,
            lbl_message
        ]
        set_font(font_list)
        
        
        
    def create_widget(self):
        return self
        
        
        
        