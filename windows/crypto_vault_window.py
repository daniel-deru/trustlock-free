from operator import itemgetter
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import re
from typing import Pattern
from datetime import date, datetime, timedelta
from json import dumps, loads
from PyQt5.QtWidgets import ( QDialog, QLineEdit, QComboBox, QListView)
from PyQt5.QtCore import pyqtSignal, Qt, QSize, pyqtSlot
from PyQt5.QtGui import QIcon


from designs.python.crypto_vault_window import Ui_CryptoVault

from widgetStyles.Dialog import Dialog
from widgetStyles.ComboBox import ComboBox
from widgetStyles.Label import Label
from widgetStyles.PushButton import PushButton, IconToolButton
from widgetStyles.LineEdit import LineEdit
from widgetStyles.ToolButton import ToolButton
from widgetStyles.QCheckBox import WhiteEyeCheckBox, BlackEyeCheckBox
from widgetStyles.Calendar import Calendar
from widgetStyles.DateEdit import DateEditForm

from utils.helpers import StyleSheet, set_font, json_to_dict
from utils.message import Message

from database.model import Model

from windows.generate_password import GeneratePasswordWindow
from windows.crypto_words import CryptoWords
from windows.group_window import GroupWindow

class CryptoVaultWindow(Ui_CryptoVault, QDialog):
    crypto_update_signal = pyqtSignal(bool)
    def __init__(self, secret=None):
        super(CryptoVaultWindow, self).__init__()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.setupUi(self)
        
        self.cmb_group.setView(QListView())
        self.cmb_group.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.cmb_num_words.setView(QListView())
        self.cmb_num_words.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.secret: tuple or None = secret
        
        self.set_groups()
        self.dte_password_exp.setDate(date.today() + timedelta(days=90))
        # self.displayWordBoxes()
        self.read_styles()
        if self.secret: self.fill_data()
        
        # Set the words if there are existing words
        if self.secret == None:
            self.words = None
        else:
            self.string_words: str = json_to_dict(self.secret[3])['words']
            self.words = self.string_words.split(" ")

        self.cmb_num_words.currentIndexChanged.connect(self.update)
        self.chk_password1.stateChanged.connect(lambda: self.show_hide_password(self.chk_password1, self.lne_password1))
        self.chk_password2.stateChanged.connect(lambda: self.show_hide_password(self.chk_password2, self.lne_password2))
        self.chk_private_key.stateChanged.connect(lambda: self.show_hide_password(self.chk_private_key, self.lne_private))
        
        self.btn_save.clicked.connect(self.save)
        self.tbtn_generate_password.clicked.connect(self.generate_password)
        self.tbtn_num_words.clicked.connect(self.open_word_window)
        self.tbtn_add_group.clicked.connect(self.add_new_group)
        
    def add_new_group(self):
        group_window = GroupWindow()
        group_window.group_add_signal.connect(lambda: self.set_groups())
        group_window.exec_()
        
    def open_word_window(self):
        words: int = self.get_num_words()
        existing_words = self.words
        
        if(self.secret and not existing_words):
            data: object = self.get_data()
            existing_words: list[str] = data['words'].split(" ")
            if words > len(existing_words):
                existing_words += ["" for _ in range(words - len(existing_words))]
            

        crypto_words_window = CryptoWords(words, existing_words)
        crypto_words_window.filled_words.connect(self.set_words)
        crypto_words_window.exec_()
        
    def set_words(self, words):
        self.words = words
        
    def set_groups(self):
        groups = Model().read("groups")
        
        groups = sorted(groups, key=itemgetter(1))
        
        self.cmb_group.clear()
        for i in range(len(groups)):
            self.cmb_group.addItem(groups[i][1], groups[i][0])
            if self.secret and int(self.secret[4]) == groups[i][0]:
                self.cmb_group.setCurrentIndex(i)
                
        for i in range(len(groups)):
            if groups[i][1] == "Ungrouped":
                self.cmb_group.setCurrentIndex(i)
        
    @pyqtSlot()
    def generate_password(self):
        GeneratePasswordWindow().exec_()
        
    def read_styles(self):
        settings = Model().read("settings")[0]
        night_mode_on = int(settings[1])
        checkbox = WhiteEyeCheckBox if night_mode_on else BlackEyeCheckBox
        widget_list = [
            checkbox, Dialog, ComboBox,
            Label, PushButton, LineEdit,
            ToolButton, Calendar, DateEditForm,
            IconToolButton("#tbtn_generate_password"),
            IconToolButton("#tbtn_num_words"),
            IconToolButton("#tbtn_add_group")
        ]
        stylesheet = StyleSheet(widget_list).create()
        
        # Set the generate password icon
        self.tbtn_generate_password.setIcon(QIcon(":/button_icons/password"))
        self.tbtn_generate_password.setIconSize(QSize(30, 20))

        self.setStyleSheet(stylesheet)
        
        font_widgets = [
            self.lbl_description, self.lbl_name, self.lbl_password,
            self.lbl_password2, self.lbl_private, self.lbl_public,
            self.lbl_words, self.lne_description, self.lne_name,
            self.cmb_num_words, self.lne_password2, self.lne_private,
            self.lne_public, self.lbl_words, self.btn_save,
            self.lne_password1, self.lbl_generate_password,
            self.lbl_password_exp, self.dte_password_exp,
            self.lbl_group, self.cmb_group, self.cmb_group.view(),
            self.cmb_num_words.view(), self.tbtn_num_words,
            self.tbtn_add_group
        ]
        
        set_font(font_widgets)       
        

    def update(self) -> None:
        self.read_styles()

    def save(self) -> None:
        password1: str = self.lne_password1.text()
        password2: str = self.lne_password2.text()

        description:str = self.lne_description.text()
        username: str = self.lne_name.text()
        
        public_key: str = self.lne_public.text()
        private_key: str = self.lne_private.text()
        password_exp = self.dte_password_exp.date().toPyDate()
        
        group = self.cmb_group.currentData()
        
        password_exp_string = datetime.strftime(password_exp, "%Y-%m-%d")

        if(password1 and (password1 != password2)):
            return Message("The passwords don't match", "Passwords Incorrect").exec_()
        elif(not description): 
            return Message("Please Provide a description", "No Description").exec_()
        elif(not username): 
            return Message("Please Provide a username", "No Username").exec_()
        elif(not self.words):
            return Message("Please save your passphrase by pressing the 'Add' button.", "No Passphrase").exec_()        

        data = {
            'name': username,
            'num_words': len(self.words),
            'words': " ".join(self.words),
            'description': description,
            'password': password1,
            "password_exp": password_exp_string
        }
            
        if private_key:
            data['private_key'] = private_key
        if public_key:
            data['public_key'] = public_key
        
        payload = {
            'type': 'crypto', 
            'name': description, 
            'data': dumps(data),
            'group_id': group
        }

        if self.secret:
            Model().update("vault", payload, self.secret[0])
        else:
            Model().save("vault", payload)

        self.crypto_update_signal.emit(True)
        self.close()
    
    def get_num_words(self) -> int:
        num_words: str = self.cmb_num_words.currentText()
        # Get the start and end index matching the regex 
        (start, end) = re.match("^\d+", num_words).span()
        # Get the number of words that needs to be represented
        words: int = int(num_words[start: end])

        return words

    def fill_data(self):
        data: object = self.get_data()
        self.lne_description.setText(data['description'])
        self.lne_password1.setText(data['password'])
        self.lne_password2.setText(data['password'])
        self.lne_name.setText(data['name'])
        
        # Get the datetime object from string
        password_exp_datetime: datetime = datetime.strptime(data['password_exp'], "%Y-%m-%d")
        
        # Get the date object from datetime object
        password_exp_date: date = date(password_exp_datetime.year, password_exp_datetime.month, password_exp_datetime.day)
        
        # Set the date
        self.dte_password_exp.setDate(password_exp_date)
        
        if 'private_key' in data:
            self.lne_private.setText(data['private_key'])
            
        if 'public_key' in data:
            self.lne_public.setText(data['public_key'])

        combobox: QComboBox = self.cmb_num_words

        # Regex to find the correct option in the drop down
        regex: Pattern[str] = f"^{str(data['num_words'])}"

        # Find and set the correct option in the drop down
        for i in range(combobox.count()):
            if(re.match(regex, combobox.itemText(i))):
                combobox.setCurrentIndex(i)
        self.update()
    
    def get_data(self) -> object:
        data: object = loads(self.secret[3])
        return data
    
    def show_hide_password(self, checkbox, line_edit):
        if checkbox.isChecked():
            line_edit.setEchoMode(QLineEdit.Normal)
        else:
            line_edit.setEchoMode(QLineEdit.Password)