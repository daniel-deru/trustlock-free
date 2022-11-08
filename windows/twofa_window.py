import os
import sys
import qrcode
import pyotp
import pyperclip
from pynput.keyboard import Key, Controller

from PyQt5.QtWidgets import QDialog, QLineEdit
from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot
from PyQt5.QtGui import QFont, QIcon, QCursor, QCloseEvent

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.twofa_window import Ui_TwoFADialog

from utils.helpers import StyleSheet, set_font
from utils.qrcode import QRCodeTemplate
from utils.message import Message
from utils.enums import TwofaStatus

from widgetStyles.Label import Label
from widgetStyles.Dialog import Dialog
from widgetStyles.ToolButton import ToolButton
from widgetStyles.PushButton import PushButton100Width
from widgetStyles.LineEdit import LineEdit

from database.model import Model

class TwofaDialog(Ui_TwoFADialog, QDialog):
    twofa_status = pyqtSignal(TwofaStatus)
    
    def __init__(self):
        super(TwofaDialog, self).__init__()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        
        self.settings = Model().read("settings")[0]
        self.night_mode_on: int = int(self.settings[1])
        self.twofa_code_valid = False
        self.otp = None
        
        self.setupUi(self)
        self.read_styles()
        self.set_icons()
        self.create_qrcode()
        self.add_slots()      
        
        self.btn_copy.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.btn_copy.clicked.connect(lambda: pyperclip.copy(self.lbl_setupkey.text()))
        self.btn_exit.clicked.connect(self.close)
        self.btn_done.clicked.connect(self.verify_code)
        
    def add_slots(self):
        
        code_input_list = [
            self.lne_code1,
            self.lne_code2,
            self.lne_code3,
            self.lne_code4,
            self.lne_code5,
            self.lne_code6
        ]
        
        for input in code_input_list:
            input.textChanged.connect(lambda: Controller().press(Key.tab))    


    def verify_code(self):
        if not self.otp:
            Message("Failure Something wrong with the setup code", "Failed to verify").exec_()
        totp = pyotp.TOTP(self.otp)
        
        code = ""
        
        for i in range(self.hbox_codes.count()):
            item: QLineEdit = self.hbox_codes.itemAt(i).widget()
            code += item.text()
            
        valid = totp.verify(code)
        
        if not valid:
            Message("The code that was entered is not correct", "Incorrect Code").exec_()
        else:
            self.twofa_code_valid = True
            self.close()
        
    def set_icons(self):
        icon = ":/input/copy_white" if self.night_mode_on else ":/input/copy_black"
        self.btn_copy.setIcon(QIcon(icon))

    def read_styles(self):
        widget_list = [Label, Dialog, ToolButton, PushButton100Width, LineEdit]

        stylesheet = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)
        
        font_widgets =[
            self.lbl_message,
            self.lbl_setupkey,
            self.btn_copy,
            self.btn_exit,
            self.lbl_enter_code_display,
            self.btn_done,
            self.lbl_setup_display
        ]
        
        set_font(font_widgets)

    def create_qrcode(self):
        self.get_otp()
        email = Model().read("user")[0][2]
        auth_string = f"otpauth://totp/TrustLock:{email}?secret={self.otp}&issuer=TrustLock"

        self.lbl_qrcode.setPixmap(qrcode.make(auth_string, image_factory=QRCodeTemplate).pixmap())

    def get_otp(self):
        self.otp = Model().read("user")[0][5]

        if self.otp == None or self.otp == "None":
            self.otp = pyotp.random_base32()
        self.lbl_setupkey.setText(self.otp)
    
    def closeEvent(self, event: QCloseEvent) -> None:
        if self.twofa_code_valid:
            Model().update("settings", {'twofa': '1'}, 'settings')
            Model().update('user', {'twofa_key': self.otp}, 'user')
            self.twofa_status.emit(TwofaStatus.success)
        else:
            self.twofa_status.emit(TwofaStatus.failure)
            
        return super().closeEvent(event)


    