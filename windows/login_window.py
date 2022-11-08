import os
import sys

from PyQt5.QtWidgets import QDialog, QLineEdit, QWidget
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QCloseEvent, QFont

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.login_window import Ui_Login
from utils.helpers import StyleSheet, LoginEvent, set_font
from database.model import Model
from utils.message import Message

from widgetStyles.Label import Label
from widgetStyles.LineEdit import LineEdit
from widgetStyles.PushButton import PushButton
from widgetStyles.Dialog import Dialog
from widgetStyles.QCheckBox import BlackEyeCheckBox, WhiteEyeCheckBox

from windows.twofa_verify_window import TwofaVerifyWindow


class Login(Ui_Login, QDialog):
    login_status = pyqtSignal(str)
    update_password_status = pyqtSignal(str)
    def __init__(self, update_password=False):
        super(Login, self).__init__()
        
        self.login_state = "failure"
        self.update_password = update_password
        # Check if the window closed from login button or exit button
        self.login_pressed = False
        
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.read_styles()
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        
        
        self.btn_login.clicked.connect(self.login)
        
        pass_field = self.lnedt_password
        show_pass = QLineEdit.Normal
        hide_pass = QLineEdit.Password
        show_password_callback = lambda show: pass_field.setEchoMode(show_pass) if show else pass_field.setEchoMode(hide_pass)
        self.chk_show_password.stateChanged.connect(show_password_callback)
        self.lnedt_password.setEchoMode(QLineEdit.Password)


    def read_styles(self):
        settings = Model().read('settings')[0]
        dark_mode_on = int(settings[1])
        font: str = settings[2]
        checkbox = WhiteEyeCheckBox if dark_mode_on else BlackEyeCheckBox
        
        styles = [
            PushButton,
            Label,
            LineEdit,
            Dialog,
            checkbox
            ]
        
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        
        font_widgets = [
            self.lbl_password,
            self.lnedt_password,
            self.btn_login
        ]
        
        set_font(font_widgets)
        
    def login(self):
        user = Model().read("user")[0]
        db_password = user[3]
        password = self.lnedt_password.text()
        has_2fa = Model().read('settings')[0][7]

        signal = self.get_correct_signal()
        
        # if the is wrong
        if(password != db_password):
            return Message("The password is incorrect", "Wrong Password").exec_()
            
        # if twofa is not required
        if(not int(has_2fa)):
            signal.emit("success")
            self.login_pressed = True
            return self.close()
        
        self.hide()
        twofa_verify_window = TwofaVerifyWindow()
        twofa_verify_window.opt_verify_signal.connect(self.verify_otp)
        twofa_verify_window.exec_()
        


    def verify_otp(self, verified):
        signal = self.get_correct_signal()
            
        if(verified == LoginEvent.success):
            signal.emit("success")
            self.login_pressed = True
            self.close()
            
    def closeEvent(self, a0: QCloseEvent) -> None:
        if not self.login_pressed:
            signal = self.get_correct_signal()
            signal.emit("failure")
        
        return super().closeEvent(a0)
    
    def show_password(self, show):
        if show: self.lnedt_password.setEchoMode(QLineEdit.Normal)
        else: self.lnedt_password.setEchoMode(QLineEdit.Password)
        
    def get_correct_signal(self):
        signal: pyqtSignal = self.login_status
        
        if(self.update_password):
            signal = self.update_password_status
            
        return signal
            
