import os
import sys
import pyotp
from pynput.keyboard import Key, Controller

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap, QCloseEvent

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.twofa_verify_window import Ui_TwofaDialog

from database.model import Model

from utils.helpers import StyleSheet, LoginEvent, set_font
from utils.message import Message

from widgetStyles.Label import Label
from widgetStyles.LineEdit import LineEdit
from widgetStyles.PushButton import ButtonFullWidth
from widgetStyles.Dialog import Dialog

class TwofaVerifyWindow(Ui_TwofaDialog, QDialog):
    opt_verify_signal = pyqtSignal(LoginEvent.event_type)
    def __init__(self):
        super(TwofaVerifyWindow, self).__init__()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.setupUi(self)
        self.read_styles()
        
        self.success = False
        
        # Set the google logo
        pixmap: QPixmap = QPixmap(":/other/google_auth_logo")
        pixmap = pixmap.scaled(40, 40)
        self.lbl_google_logo.setPixmap(pixmap)
        
        
        self.code: str = ""
        
        self.lne_code_1.setFocus()
        
        self.text_field_list = [
            self.lne_code_1,
            self.lne_code_2,
            self.lne_code_3,
            self.lne_code_4,
            self.lne_code_5,
        ]
        
        for text_field in self.text_field_list:
            text_field.textChanged.connect(self.change_lines)
            
        self.lne_code_6.textChanged.connect(self.verify_otp)

    def read_styles(self):
        widget_list = [ButtonFullWidth, LineEdit, Label, Dialog]

        stylesheet = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)
        
        font_widgets = [
            self.lbl_message
        ]
        
        set_font(font_widgets)

    def verify_otp(self, value):
        # Get the otp from the database
        code: str = Model().read('user')[0][5]
        totp: str or int = pyotp.TOTP(code)
        
        # Add the last digit from the last text field
        self.code += value
        # If there aren't 6 digits don't continue process
        if len(self.code) < 6: return
        
        # Verify the code
        if(totp.verify(self.code)):
            self.success = True
            self.opt_verify_signal.emit(LoginEvent.success)
            self.close()
        else:
            for field in self.text_field_list:
                field.clear()
            
            Message("The code is invalid.", "Invalid Code").exec_()
            
            # Reset the window
            self.lne_code_1.setFocus()
            self.opt_verify_signal.emit(LoginEvent.failed)
        
        self.code = ""
            
    def change_lines(self, value):
        self.code += value
        Controller().press(Key.tab)
        
    def closeEvent(self, event: QCloseEvent) -> None:
        if not self.success:
            self.opt_verify_signal.emit(LoginEvent.closed)
        return super().closeEvent(event)

        

