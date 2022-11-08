import os
import sys
import json

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon, QCloseEvent

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.drive_window import Ui_DriveDialog

from widgetStyles.PushButton import PushButton
from widgetStyles.QCheckBox import CheckBoxSquare
from widgetStyles.Dialog import Dialog

from utils.helpers import StyleSheet, set_font
from utils.globals import PATH
from utils.message import Message

from database.model import Model


class DriveWindow(Ui_DriveDialog, QDialog):
    drive_dict = pyqtSignal(object)
    def __init__(self):
        super(DriveWindow, self).__init__()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setupUi(self)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.read_styles()
        
        self.btn_save.clicked.connect(self.save)
        
        self.chk_google.stateChanged.connect(self.check_google)
        
        self.data_saved = False
        
        self.set_checkboxes()
    
    def set_checkboxes(self):
        json_settings = Model().read("settings")[0][8]
        settings = json.loads(json_settings)
        
        self.chk_google.setChecked(settings['google'])
        self.chk_onedrive.setChecked(settings['onedrive'])
        
    def check_google(self, state):
        token_file = f"{PATH}/integrations/google_token.json"
        if not os.path.exists(token_file) and self.chk_google.checkState() == Qt.Checked:
            Message("Please Allow Trust Lock to integrate with your google account by clicking on The 'Sign in with Google' button", "Not Allowed").exec_()
            self.chk_google.setChecked(False)
            self.chk_google.setCheckState(Qt.Unchecked)
            
        
    def read_styles(self):
        widget_list = [PushButton, CheckBoxSquare, Dialog]
        
        stylesheet = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)
        
        font_widgets = [
            self.chk_google,
            self.chk_onedrive,
            self.btn_save
        ]
        
        set_font(font_widgets)
        
    def save(self):
        drives = {
            'google': self.chk_google.isChecked(),
            'onedrive': self.chk_onedrive.isChecked()
        }
        self.data_saved = True
        self.drive_dict.emit(drives)
        self.close()
        
    def closeEvent(self, event: QCloseEvent) -> None:
        if not self.data_saved: self.drive_dict.emit(None)
        return super().closeEvent(event)
        