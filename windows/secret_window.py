from operator import itemgetter
import os
import sys
import json

from PyQt5.QtWidgets import QDialog, QWidget, QListView
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QFont
from cryptography.fernet import Fernet

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.vault_add_window import Ui_AddSecret_window

from database.model import Model

from widgetStyles.PushButton import PushButton, IconToolButton
from widgetStyles.SpinBox import SpinBox
from widgetStyles.Label import Label
from widgetStyles.LineEdit import LineEdit
from widgetStyles.Dialog import Dialog
from widgetStyles.ComboBox import ComboBox

from utils.helpers import StyleSheet, json_to_dict, set_font
from utils.message import Message

from windows.group_window import GroupWindow

class SecretWindow(Ui_AddSecret_window, QDialog):
    secret_signal = pyqtSignal(str)
    def __init__(self, secret=None):
        
        super(SecretWindow, self).__init__()
        self.secret = secret if secret else None
        self.setupUi(self)
        self.set_groups()
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.cmb_group.setView(QListView())
        self.cmb_group.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.read_styles()
        self.btn_save.clicked.connect(self.save)
        self.btn_cancel.clicked.connect(lambda: self.close())
        self.tbtn_add_group.clicked.connect(self.add_new_group)
       
        if secret:
            self.display_secret()
        
    def add_new_group(self):
        group_window = GroupWindow()
        group_window.group_add_signal.connect(lambda: self.set_groups())
        group_window.exec_()
            
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

    
    def display_secret(self):
        data: object = json_to_dict(self.secret[3])
        keys: list[str] = list(data.keys())
        values: list[str] = list(data.values())
        container = self.vbox_column_def
        self.lnedt_name.setText(self.secret[2])

        for i in range(len(keys)):
            # Set the data to the fields
            container.itemAt(i).layout().itemAt(0).widget().setText(keys[i])
            container.itemAt(i).layout().itemAt(1).widget().setText(values[i])


    def get_data(self) -> object:
        data: object = {}
        fields = self.vbox_column_def.layout()
        
        name = self.lnedt_name.text()
        if not name:
            Message("Please enter a display name for your secret by which your will recognize it.", "No Name Entered").exec_()
            return False
        
        for i in range(fields.count()):
            field = fields.itemAt(i).layout()
            header_field = field.itemAt(0).widget()
            data_field = field.itemAt(1).widget()


            if not header_field.text() and data_field.text():
                Message("One or more of your data entries is missing a header. Please", "Please check your information.").exec_()
                return False
            elif header_field.text() and not data_field.text():
                Message("One or more of your header fields is missing a data entry.", "Please check your information.").exec_()
                return False
            elif header_field.text() and data_field.text():
                data[header_field.text()] = data_field.text()
            
        return {
            'name': name,
            'data': data
        }


    def save(self) -> None:
        group = self.cmb_group.currentData()
        data = self.get_data()
        
        if not data: return
        if(len(data['data'].keys()) <= 0):
            Message("Please Enter data into the vault.", "No Data").exec_()
            return
        
        payload = {
            'type': 'general', 
            'name': data['name'], 
            'data': json.dumps(data["data"]),
            'group_id': group
        }
        # The secret does not exist in the database (save the secret)
        if not self.secret:
            Model().save('vault', payload)
        # The secret does exist (update the secret)
        elif self.secret:
            Model().update("vault", payload, self.secret[0])
            
        self.secret_signal.emit("saved")
        self.close()
    
    def encrypt(self, data):
                # Convert data to json
        json_data = json.dumps(data)
        # Generate Random Key
        key = Fernet.generate_key()
        f = Fernet(key)

        # Convert the json data to bytes and encrypt with secret key
        secret = f.encrypt(json_data.encode("UTF-8"))

        return {
            'secret': secret,
            'key': key
            }

    def read_styles(self) -> None:
        styles = [
            PushButton,
            SpinBox,
            Label,
            LineEdit,
            Dialog,
            ComboBox,
            IconToolButton("#tbtn_add_group")
        ]

        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        
        font_widgets = [
            self.lbl_name,
            self.lbl_data,
            self.lbl_headers,
            self.btn_cancel,
            self.btn_save,
            self.lnedt_name,
            self.lnedt_data1,
            self.lnedt_data2,
            self.lnedt_data3,
            self.lnedt_data4,
            self.lnedt_data5,
            self.lnedt_header1,
            self.lnedt_header2,
            self.lnedt_header3,
            self.lnedt_header4,
            self.lnedt_header5,
            self.lbl_group,
            self.cmb_group,
            self.cmb_group.view(),
            self.tbtn_add_group,
        ]

        set_font(font_widgets)