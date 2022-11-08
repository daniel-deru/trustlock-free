import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QCursor, QIcon

from database.model import Model

from widgetStyles.PushButton import VaultButton
from widgetStyles.styles import VAULT_BUTTON_COLORS

from utils.helpers import set_font

class VaultItem(QPushButton):
    vault_clicked_signal = pyqtSignal(tuple)
    def __init__(self, secret):
        super(VaultItem, self).__init__()
        self.secret = secret
        self.setupUI()
        self.read_styles()
        self.setCursor(QCursor(Qt.PointingHandCursor))
    
        self.clicked.connect(self.app_clicked)

    def app_clicked(self):
        self.vault_clicked_signal.emit(tuple(self.secret))

    def create(self):
        return self
    
    def setupUI(self):
        self.setText(self.secret[2])

        set_font([self])
        
        icon = QIcon(f":/button_icons/{self.secret[1]}")
        self.setIcon(icon)
    
    def read_styles(self):
        color = VAULT_BUTTON_COLORS[self.secret[1]]
        self.setStyleSheet(VaultButton(color))

        