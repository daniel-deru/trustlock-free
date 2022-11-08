import sys
import os

from widgetStyles.TextEdit import TextEdit
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot, QSize
from PyQt5.QtGui import QFont, QIcon


from designs.python.group_window import Ui_GroupWindow

from utils.message import Message

from database.model import Model

from utils.helpers import StyleSheet, set_font

from widgetStyles.Label import Label
from widgetStyles.PushButton import PushButton
from widgetStyles.Dialog import Dialog
from widgetStyles.LineEdit import LineEdit

class GroupWindow(Ui_GroupWindow, QDialog):
    group_add_signal = pyqtSignal(bool)
    def __init__(self, group=None) -> None:
        super(GroupWindow, self).__init__()
        self.setupUi(self)
        self.read_styles()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.group = group
        
        if self.group: self.fill_data()
        
        self.btn_discard.clicked.connect(self.close)
        self.btn_save.clicked.connect(self.save)
        
    def read_styles(self):
        widget_list = [Dialog, PushButton, Label, LineEdit, TextEdit]
        
        stylesheet = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)
        
        font_list = [
            self.lbl_description,
            self.lbl_name,
            self.lne_description,
            self.lne_name,
            self.btn_discard,
            self.btn_save
        ]
        set_font(font_list)
        
    def fill_data(self):
        self.lne_name.setText(self.group['name'])
        self.lne_description.setText(self.group['description'])
        self.btn_save.setText("Update")
    
    @pyqtSlot()
    def save(self):
        name = self.lne_name.text()
        description = self.lne_description.toPlainText()
        
        if not name:
            Message("Please enter a name for the group", "Missing Group Name").exec_()
            
        group = {
            "name": name,
            "description": description
        }
        
        if not self.group:
            Model().save("groups", group)
        else:
            Model().update("groups", group, self.group['id'])
        self.group_add_signal.emit(True)
        self.close()
            
        
        
        