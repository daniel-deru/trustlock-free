import sys
import os
from json import dumps

from PyQt5.QtWidgets import (
    QDialog, 
    QLabel, 
    QSpacerItem, 
    QSizePolicy, 
    QToolButton, 
    QCheckBox, 
    QHBoxLayout, 
    QVBoxLayout, 
    QFrame,
    QMessageBox
)
from PyQt5.QtCore import pyqtSignal, Qt, QSize, pyqtSlot
from PyQt5.QtGui import QIcon, QCursor, QFont, QCloseEvent
import pyperclip

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.general_vault_view_window import Ui_GeneralVaultView

from widgetStyles.Label import Label
from widgetStyles.ToolButton import ToolButton
from widgetStyles.QCheckBox import WhiteEyeCheckBox, BlackEyeCheckBox
from widgetStyles.Dialog import Dialog
from widgetStyles.PushButton import PushButton

from utils.helpers import StyleSheet, json_to_dict, clear_window
from utils.message import Message

from windows.secret_window import SecretWindow

from database.model import Model

class GeneralVaultView(Ui_GeneralVaultView, QDialog):
    update_signal = pyqtSignal(bool)
    def __init__(self, secret) -> None:
        super(GeneralVaultView, self).__init__()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        settings = Model().read('settings')[0]
        self.night_mode_on = int(settings[1])
        self.font_name = settings[2]
        self.secret = secret
        self.data = json_to_dict(secret[3])
        self.setupUi(self)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.read_styles()
        self.set_data()
        
        self.should_update = False
        
        self.btn_delete.clicked.connect(self.delete_secret)
        self.btn_edit.clicked.connect(self.edit_secret)
    
    @pyqtSlot()
    def delete_secret(self):
        confirm_delete = Message("Are you sure you want to delete this data", "Are You Sure?").prompt()
        
        if confirm_delete == QMessageBox.No: return
        
        Model().delete("vault", self.secret[0])
        self.should_update = True
        self.close()
    
    @pyqtSlot()
    def edit_secret(self):
        edit_window = SecretWindow(self.secret)
        edit_window.secret_signal.connect(self.update_after_edit)
        edit_window.exec_()
        
    @pyqtSlot()
    def update_after_edit(self):
        # Get the new secrets
        secrets: list[list] = Model().read("vault")
        # Filter to get the correct one
        secret_filter = filter(lambda secret: secret[0] == self.secret[0], secrets)
        # get list object from filter object
        secret = list(secret_filter)[0]
        # Set the new data
        self.secret = secret
        self.data = json_to_dict(secret[3])
        
        self.set_data()
        
        self.should_update = True
        
        
    def read_styles(self):
        
        checkbox = WhiteEyeCheckBox if self.night_mode_on else BlackEyeCheckBox
        
        widget_list = [
            checkbox,
            Label,
            ToolButton,
            Dialog,
            PushButton
        ]
        
        stylesheet = StyleSheet(widget_list).create()
        
        self.setStyleSheet(stylesheet)
        
        self.lbl_description.setFont(QFont(self.font_name))
        self.btn_edit.setFont(QFont(self.font_name))
        self.btn_delete.setFont(QFont(self.font_name))
        
    def set_data(self):
        self.lbl_description.setText(self.secret[2])
        
        keys: list[str] = list(self.data.keys())
        values: list[str] = list(self.data.values())
        
        clear_window(self.vbox_secrets)
        
        for i in range(len(keys)):
            widget = self.create_widget(keys[i], values[i])
            self.vbox_secrets.addWidget(widget)
        
    def create_widget(self, key: str, value: str) -> QFrame:
        frame: QFrame = QFrame()
        frame.setObjectName("view_frame")
        hbox = QHBoxLayout()
        
        lbl_key: QLabel = QLabel(key)
        lbl_key.setFont(QFont(self.font_name))
        lbl_key.setMinimumWidth(200)
        
        lbl_value: QLabel = QLabel(u"\u2022"*10)
        lbl_value.setFont(QFont(self.font_name))
        
        hspacer: QSpacerItem = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        btn_copy: QToolButton = QToolButton()
        icon_path = ":/input/copy_white" if self.night_mode_on else ":/input/copy_black"
        btn_copy.setIcon(QIcon(icon_path))
        btn_copy.setIconSize(QSize(20, 20))
        btn_copy.setCursor(QCursor(Qt.PointingHandCursor))
        btn_copy.clicked.connect(lambda: self.copy(key))
        
        btn_view: QCheckBox = QCheckBox()
        btn_view.setCursor(QCursor(Qt.PointingHandCursor))
        btn_view.stateChanged.connect(lambda checked: self.view(key, checked, lbl_value))
        
        hbox.addWidget(lbl_key)
        hbox.addWidget(lbl_value)
        hbox.addItem(hspacer)
        hbox.addWidget(btn_copy)
        hbox.addWidget(btn_view)
        
        vbox: QVBoxLayout = QVBoxLayout()
        
        hline: QFrame = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)
        hline.setStyleSheet("background: #9ecd16;")
        hline.setMaximumHeight(1)
        
        vbox.addLayout(hbox)
        vbox.addWidget(hline)
        
        frame.setLayout(vbox)
        return frame
    
    def copy(self, field_name):
        pyperclip.copy(self.data[field_name])
        
    def view(self, key: str, checked: bool, lbl_value: QLabel):
        if checked:
            lbl_value.setText(self.data[key])
        else:
            lbl_value.setText(u"\u2022"*10)
            
    def closeEvent(self, event: QCloseEvent) -> None:
        if self.should_update:
            self.update_signal.emit(True)
            
        return super().closeEvent(event)
        
        
        