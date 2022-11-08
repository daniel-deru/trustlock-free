import os
import sys

from widgetStyles.Label import Label
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QFont

from widgetStyles.PushButton import PushButton
from widgetStyles.Dialog import Dialog

from utils.helpers import StyleSheet, set_font

from database.model import Model

from designs.python.backup_verify import Ui_backup_verify


class BackupVerifyWindow(Ui_backup_verify, QDialog):
    yes_signal = pyqtSignal(bool)
    def __init__(self) -> None:
        super(BackupVerifyWindow, self).__init__()
        self.setupUi(self)
        # self.setFixedHeight(300)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.read_styles()
        
        self.btn_no.clicked.connect(lambda: self.response(False))
        self.btn_yes.clicked.connect(lambda: self.response(True))
        
    def read_styles(self):
        widget_list = [
            Dialog,
            Label,
            PushButton
        ]
        stylesheet = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)
        
        font_list = [
            self.btn_no,
            self.btn_yes,
            self.lbl_explain,          
            self.lbl_heading,
            self.lbl_keys,
            self.lbl_liability,
            self.lbl_warning,
            self.lbl_reccomend
        ]
        
        set_font(font_list)
        
        self.lbl_warning.setStyleSheet("color: red; font-size: 48px")
        self.lbl_heading.setStyleSheet("color: red; font-size: 24px; margin-bottom: 10px;")
        self.lbl_liability.setStyleSheet("color: red; font-size: 20px")
        self.lbl_keys.setStyleSheet("font-size: 24px;")

    
    def response(self, response):
        self.close()
        self.yes_signal.emit(response)
        return response