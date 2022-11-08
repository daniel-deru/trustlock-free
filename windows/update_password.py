import json
import sys
import os
from datetime import date, datetime, timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QDialog, QMessageBox, QLineEdit, QWidget
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSize, Qt
from PyQt5.QtGui import QIcon, QFont

from designs.python.update_password import Ui_UpdatePassword

from database.model import Model

from utils.message import Message
from utils.helpers import StyleSheet, set_font

from widgetStyles.Dialog import Dialog
from widgetStyles.DateEdit import DateEditForm
from widgetStyles.PushButton import PushButton, IconToolButton
from widgetStyles.QCheckBox import EyeCheckBox
from widgetStyles.Label import Label
from widgetStyles.LineEdit import LineEdit
from widgetStyles.Frame import FrameContainer

from windows.generate_password import GeneratePasswordWindow

class UpdatePassword(Ui_UpdatePassword, QDialog):
    finished: pyqtSignal = pyqtSignal(bool)
    def __init__(self, data) -> None:
        super(UpdatePassword, self).__init__()
        self.setupUi(self)
        self.read_styles()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.data = data
        self.queue = [self.data.pop(-1)]
        self.dte_password_exp.setDate(date.today() + timedelta(days=90))
        self.show_item()
        
        self.btn_same.clicked.connect(self.same_password)
        self.btn_save.clicked.connect(self.save_password)
        self.tbtn_password_generator.clicked.connect(self.generate_password)
        
        self.chk_show_password1.stateChanged.connect(lambda state: self.show_password(state, self.lne_password1))
        self.chk_show_password2.stateChanged.connect(lambda state: self.show_password(state, self.lne_password2))
        
    @pyqtSlot()
    def generate_password(self):
        GeneratePasswordWindow().exec_()

    
    @pyqtSlot()   
    def save_password(self):
        password1: str = self.lne_password1.text()
        password2: str = self.lne_password2.text()
        exp_date = self.dte_password_exp.date().toPyDate()
        
        exp_date_string: str = datetime.strftime(exp_date, "%Y-%m-%d")
        
        if password1 != password2:
            Message("New Password and Confirm Password are not the same", "Passwords Don't Match").exec_()
            return
        
        table, item = self.queue[0]
        id = item[0]
        
        if table == "user":
            Model().update(table, {"password": password1, "password_exp": exp_date_string}, id)
        else:
            data_object = json.loads(item[3])
            
            data_object['password'] = password1
            data_object['password_exp'] = exp_date_string
            
            json_object = json.dumps(data_object)
            
            Model().update(table, {"data": json_object}, id)
            
        self.next_password()
        self.finished.emit(True)
        
            
            
        
    def read_styles(self):
        widget_list = [
            Label,
            DateEditForm,
            Dialog,
            PushButton,
            EyeCheckBox,
            LineEdit,
            FrameContainer("#frame_account"),
            IconToolButton()
        ]
        
        stylesheet = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)
        
        font_list = [
            self.lbl_desc,
            self.lbl_account,
            self.lbl_account_display,
            self.lbl_generate_password,
            self.lbl_password1,
            self.lbl_password2,
            self.lne_password1,
            self.lne_password2,
            self.lbl_password_exp,
            self.dte_password_exp,
            self.btn_same,
            self.btn_save
        ]
        
        set_font(font_list)
        
        self.tbtn_password_generator.setIcon(QIcon(":/button_icons/password"))
        self.tbtn_password_generator.setIconSize(QSize(30, 20))
    
    @pyqtSlot()
    def same_password(self):
        table, item = self.queue[0]
        id = item[0]
        next_date = date.today() + timedelta(days=90)
        next_date_string = datetime.strftime(next_date, "%Y-%m-%d")
        
        if table == "user":
            Model().update(table, {"password_exp": next_date_string}, id)
        else:
            data_object = json.loads(item[3])

            data_object['password_exp'] = next_date_string
            
            json_object = json.dumps(data_object)
            
            Model().update(table, {"data": json_object}, id)
        
        self.next_password()
            

    def show_item(self):
        table, item = self.queue[0]
        if table == "user":
            account = "Trust Lock"
        else:
            account = item[2]
            
        self.lbl_account_display.setText(account)
    
    def show_password(self, checked, field: QLineEdit):
        if not checked:
            field.setEchoMode(QLineEdit.Password)
        else:
            field.setEchoMode(QLineEdit.Normal)
            
    def next_password(self):
        if len(self.data) == 0:
            self.close()
            return
        self.queue.pop()
        self.queue.append(self.data.pop(-1))
        self.show_item()
        self.clear_fields()
    
    def clear_fields(self):
        self.lne_password1.clear()
        self.lne_password2.clear()
            
        
    