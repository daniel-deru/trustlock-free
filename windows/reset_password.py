import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from winsound import PlaySound
import winsound

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, pyqtSlot, QSize, pyqtSignal
from PyQt5.QtGui import QIcon


from designs.python.reset_password import Ui_ResetPassword

from utils.helpers import StyleSheet, set_font

from widgetStyles.Dialog import Dialog
from widgetStyles.Label import Label
from widgetStyles.LineEdit import LineEdit
from widgetStyles.PushButton import PushButton, IconToolButton

from database.model import Model

from windows.generate_password import GeneratePasswordWindow


class ResetPassword(Ui_ResetPassword, QDialog):
    reset_signal: pyqtSignal = pyqtSignal(bool)
    def __init__(self, reset: bool = True):
        super(ResetPassword, self).__init__()
        self.reset = reset
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.setupUi(self)
        self.read_styles()

        self.btn_reset.clicked.connect(self.compare_passwords)
        self.tbtn_password_generator.clicked.connect(self.generate_password)
        
    @pyqtSlot()
    def generate_password(self):
        GeneratePasswordWindow().exec_()

    def read_styles(self):
        widgetlist: list[str] = [
            Dialog,
            Label,
            LineEdit,
            PushButton,
            IconToolButton()
        ]

        stylesheet: str = StyleSheet(widgetlist).create()
        self.setStyleSheet(stylesheet)
        
        self.tbtn_password_generator.setIcon(QIcon(":/button_icons/password"))
        self.tbtn_password_generator.setIconSize(QSize(30, 20))
        
        font_list = [
            self.lbl_confirm_password,
            self.lbl_password1,
            self.lbl_message,
            self.btn_reset,
            self.lnedit_confirm_password,
            self.lnedt_password1,
            self.lbl_password_generator
        ]
        set_font(font_list)

    def compare_passwords(self):
        pass1 = self.lnedt_password1.text()
        pass2 = self.lnedit_confirm_password.text()
        
        if(not pass1 or not pass2):
            self.lbl_message.setText("Please enter a password.")
        elif(pass1 != pass2):
            self.lbl_message.setText("The passwords don't match.")
            PlaySound("sound.wav", winsound.SND_FILENAME)
        else:
            Model().update('user', {'password': pass1}, 'user')
            if self.reset:
                Model().update('user', {'twofa_key': None}, 'user')
                Model().update('settings', {'twofa': '0'}, 'settings')
                self.reset_signal.emit(True)
            self.close()
            