import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import pyperclip
import math
import re
from datetime import date, timedelta

from PyQt5.QtWidgets import QDialog, QLineEdit, QGridLayout, QWidget, QGraphicsBlurEffect, QWidget
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, pyqtSignal, QSize, pyqtSlot


from designs.python.new_user_tab import Ui_new_user
from database.model import Model
from windows.backup_verify import BackupVerifyWindow

from widgets.register_word import RegisterWordButton

from widgetStyles.PushButton import PushButton, IconToolButton
from widgetStyles.LineEdit import LineEdit
from widgetStyles.Label import Label
from widgetStyles.Dialog import Dialog
from widgetStyles.Widget import SideWidget
from widgetStyles.QCheckBox import BlackEyeCheckBox
from widgetStyles.Calendar import Calendar
from widgetStyles.DateEdit import DateEditForm

from utils.helpers import StyleSheet, random_words, set_font
from utils.message import Message

from windows.generate_password import GeneratePasswordWindow

from utils.enums import ServerConnectStatus, RegisterStatus

class NewUserTab(Ui_new_user, QDialog):
    register_close_signal = pyqtSignal(RegisterStatus)
    def __init__(self):
        super(NewUserTab, self).__init__()
        self.setupUi(self)
        
        self.passphrase_safe = False
        self.dte_password_exp.setDate(date.today() + timedelta(days=90))
        
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.lnedt_password.setEchoMode(QLineEdit.Password)
        self.lnedt_password2.setEchoMode(QLineEdit.Password)
        
        words = self.set_random_words()
        self.read_styles()
        
        self.btn_register.clicked.connect(self.register_clicked)
        self.btn_copy.clicked.connect(lambda: pyperclip.copy(words))
        self.tbtn_generate_password.clicked.connect(self.generate_password)
        
        self.chk_password.stateChanged.connect(lambda: self.show_hide_password(self.lnedt_password, self.chk_password))
        self.chk_password2.stateChanged.connect(lambda: self.show_hide_password(self.lnedt_password2, self.chk_password2))
        
        word_widget: QWidget = self.word_widget
        word_widget.setAttribute(Qt.WA_Hover, True)
        
        word_widget.enterEvent = self.mouseHover
        word_widget.leaveEvent = self.mouseLeave
        
        self.set_blur()
    
    @pyqtSlot()
    def generate_password(self):
        GeneratePasswordWindow().exec_()
    
    def verify_password_strength(self, password):
        contains_num = r"^.*\d+.*$"
        contains_special = r"^.*[!@#$%^&*(){}:;'\"<,>.?/\\]+.*"
        contains_upper = r".*[A-Z]+.*"
        contains_lower = r".*[a-z]+.*"
        longer_than_8 = r".{8,}"
        
        test_list = [
            [contains_num, "Password must contain a number."],
            [contains_special, "Password must contain a special character"],
            [contains_upper, "Password must contain an uppercase letter."],
            [contains_lower, "Password must contain an lowercase letter."],
            [longer_than_8, "Password must be longer than eight characters."],
        ]
        
        for test in test_list:
            pattern, message = test
            if(not re.match(pattern, password)):
                return [False, message]
        
        return [True, None]
    
    def verify_email(self, email):
        valid_email = r"^.+@[a-z]{2,12}\.[a-z]{2,10}(\.[a-z]{2,10})?$"
          
        if(re.match(valid_email, email)):
            return True

    def register_clicked(self):
        
        name = self.lnedt_name.text()
        email = self.lnedt_email.text()
        password1 = self.lnedt_password.text()
        password2 = self.lnedt_password2.text()
        password_exp = self.dte_password_exp.date().toPyDate()
        
        valid_mail = self.verify_email(email)
        valid_password, password_message = self.verify_password_strength(password1)
        
        fields = [
            name,
            email,
            password1,
            password2,
        ]
        
        for field in fields:
            if not field:
                return Message(f"Make sure you fill in all the fields.", "Please fill in all the fields").exec_()
                    
        if(not valid_mail):
            return Message("Please enter a valid email", "Email not valid").exec_()
        elif(not valid_password):
           return Message(password_message, "Password Too Weak").exec_()      
        elif password1 != password2:
            return Message("Please make sure your passwords match. Check to see if your caps lock is on", "Passwords don't match").exec_()

        data = {
            "id": "user",
            "name": name,
            "email": email,
            "password": password1,
            "passphrase": self.words,
            "password_exp": password_exp
        }
        
        message = BackupVerifyWindow()
        message.yes_signal.connect(self.set_passphrase_safe)
        message.exec_()
        
        if not self.passphrase_safe: return

        Model().save("user", data)
        self.register_close_signal.emit(RegisterStatus.user_created)
    
    def set_passphrase_safe(self, response):
        self.passphrase_safe = response

    def read_styles(self):
        styles = [
            PushButton,
            Label,
            LineEdit,
            Dialog,
            SideWidget,
            BlackEyeCheckBox,
            DateEditForm,
            Calendar,
            IconToolButton()
        ]

        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        

        self.lbl_passphrase_desc.setStyleSheet("font-weight: 700;")
        
        self.tbtn_generate_password.setIcon(QIcon(":/button_icons/password"))
        self.tbtn_generate_password.setIconSize(QSize(30, 20))
        
        font_widgets = [
            self.lbl_email,
            self.lbl_name,              self.lbl_passphrase_desc,
            self.lbl_password,          self.lbl_password2,
            self.lnedt_email,
            self.lnedt_name,            self.lnedt_password,
            self.lnedt_password2,       self.btn_copy,
            self.btn_register,          self.lbl_generate_password,
            self.lbl_password_exp,      self.dte_password_exp
        ]
        
        set_font(font_widgets)
            
    def set_random_words(self):
        random: list[str] = random_words()
        string: str = " ".join(random)
        container: QGridLayout = self.gbox_words
        
        count = 1
        for i in range(math.floor(len(random)/4)):
            for j in range(4):
                button: RegisterWordButton = RegisterWordButton(random[count - 1], count)                
                container.addWidget(button, i, j)
                count += 1
                
        self.words = string
        return string
    
    def show_hide_password(self, line_edit, checkbox):
        if checkbox.isChecked():
            line_edit.setEchoMode(QLineEdit.Normal)
        else:
            line_edit.setEchoMode(QLineEdit.Password)
                    
    def mouseHover(self, event):
        blur: QGraphicsBlurEffect = QGraphicsBlurEffect()
        blur.setBlurRadius(0)
        word_widget: QWidget = self.word_widget      
        word_widget.setGraphicsEffect(blur)
        
    def mouseLeave(self, event):
        self.set_blur()
        
    def set_blur(self):
        blur: QGraphicsBlurEffect = QGraphicsBlurEffect()
        blur.setBlurRadius(10)
        word_widget: QWidget = self.word_widget
        word_widget.setGraphicsEffect(blur)
    
    def copy_word(self, some):
        pass
    
    def create_tab(self):
        return self