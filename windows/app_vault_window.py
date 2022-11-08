from operator import itemgetter
import sys
import os
import cv2
import re
from json import dumps
from datetime import date, datetime, timedelta

from PyQt5.QtWidgets import QDialog, QFileDialog, QLineEdit, QListView
from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot, QSize
from PyQt5.QtGui import QFont, QIcon

from windows.group_window import GroupWindow

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE'], 'Desktop'))

from designs.python.app_vault_window import Ui_AppVault

from widgetStyles.Dialog import Dialog
from widgetStyles.PushButton import PushButton, IconToolButton
from widgetStyles.LineEdit import LineEdit
from widgetStyles.Label import Label
from widgetStyles.SpinBox import SpinBox
from widgetStyles.DateEdit import DateEditForm
from widgetStyles.Calendar import Calendar
from widgetStyles.ComboBox import ComboBox

from utils.helpers import StyleSheet, json_to_dict, get_checkbox, set_font
from utils.message import Message

from database.model import Model

from windows.generate_password import GeneratePasswordWindow

class AppVaultWindow(Ui_AppVault, QDialog):
    app_update_signal = pyqtSignal(bool)
    def __init__(self, app=None):
        super(Ui_AppVault, self).__init__()
        self.app = app
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.cmb_group.setView(QListView())
        self.cmb_group.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.secrets = list(filter(lambda a: a[1] == "app", Model().read("vault")))
        self.set_groups()
        
        self.dte_password_exp.setDate(date.today() + timedelta(days=90))
        
        # Get the current apps to avoid collisions
        self.current_apps = self.get_current_apps()        
        self.lne_password.setEchoMode(QLineEdit.Password)
        

        if self.app: self.fill_data()
        
        self.read_styles()
        self.btn_save.clicked.connect(self.save)
        self.tbtn_desktop.clicked.connect(self.add_from_desktop)
        self.tbtn_password_generator.clicked.connect(self.generate_password)
        self.tbtn_qrcode.clicked.connect(self.read_qrcode)
        
        self.chk_show_password.stateChanged.connect(lambda show: self.show_password(show, self.lne_password))
        self.chk_password2.stateChanged.connect(lambda show: self.show_password(show, self.lne_password2))
        
        self.tbtn_add_group.clicked.connect(self.add_new_group)
        
    def add_new_group(self):
        group_window = GroupWindow()
        group_window.group_add_signal.connect(lambda: self.set_groups())
        group_window.exec_()
        
    @pyqtSlot()
    def read_qrcode(self):
        file = QFileDialog.getOpenFileName(self, "Open a file", DESKTOP, "All Files (*.*)")[0]
        image = cv2.imread(file)
        detector = cv2.QRCodeDetector()
        code = detector.detectAndDecode(image)[0]
        if not code:
            Message("The QR code is invalid please select a valid image of a QR code", "Invalid QR Code").exec_()
            return
        
        regex = r"(?<=secret=)[0-9A-Z]+"
        result = re.search(regex, code)
        self.lne_twofa_code.setText(result.group())
    
    def set_groups(self):
        groups = Model().read("groups")
        
        groups = sorted(groups, key=itemgetter(1))
        
        self.cmb_group.clear()
        
        for i in range(len(groups)):
            self.cmb_group.addItem(groups[i][1], groups[i][0])
            if self.app and int(self.app[4]) == groups[i][0]:
                self.cmb_group.setCurrentIndex(i)
                
        for i in range(len(groups)):
            if groups[i][1] == "Ungrouped":
                self.cmb_group.setCurrentIndex(i)
    
    @pyqtSlot()
    def generate_password(self):
        GeneratePasswordWindow().exec_()
        

    def read_styles(self):
        checkbox = get_checkbox()
        widget_list = [
            Label,
            Dialog,
            PushButton,
            LineEdit,
            SpinBox,
            checkbox,
            Calendar,
            DateEditForm,
            IconToolButton(),
            ComboBox
        ]

        stylesheet: str = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)
        
        self.tbtn_password_generator.setIcon(QIcon(":/button_icons/password"))
        self.tbtn_password_generator.setIconSize(QSize(30, 20))
        
        font_widget = [
            self.lbl_email,         self.lbl_name,          
            self.lbl_password,      self.lbl_path,          
            self.lbl_username,      self.lne_email,
            self.lne_name,          self.lne_password,
            self.lne_path,          self.lne_username,
            self.tbtn_desktop,       self.btn_save,
            self.lbl_password2,     self.lne_password2,
            self.lbl_password_generator,
            self.lbl_password_expiration,
            self.dte_password_exp,
            self.lbl_group,         self.cmb_group,
            self.cmb_group.view(),  self.lbl_twofa_code,
            self.lne_twofa_code, self.tbtn_add_group
        ]
        
        set_font(font_widget)
        
        self.tbtn_desktop.setIcon(QIcon(":/button_icons/file_white"))
        self.tbtn_qrcode.setIcon(QIcon(":/button_icons/qrcode"))

    def save(self):
        
        name: str = self.lne_name.text()
        path: str = self.lne_path.text()

        username: str = self.lne_username.text()
        email: str = self.lne_email.text()
        password: str = self.lne_password.text()
        confirm_password: str = self.lne_password2.text()
        password_exp = self.dte_password_exp.date().toPyDate()
        
        twofa_key = self.lne_twofa_code.text()
        group = self.cmb_group.currentData()
        
        password_exp_string = datetime.strftime(password_exp, "%Y-%m-%d")

        name_list: list[str] = ["name", "index", "path", "username", "email", "password"]
        data_list: list[str] = [ name, "1", path, username, email, password ]

        valid_submit: bool = True

        for i in range(len(data_list)):
            if(not data_list[i]):
                Message(f"Please add {name_list[i]}", f"Missing {name_list[i]}").exec_()
                valid_submit = False
                
        if not self.app and name in self.current_apps:
            Message(f"An App with this name already exists", "App already exists").exec_()
            valid_submit = False

        if valid_submit:
            data: str = dumps({
                'name': name,
                'sequence': "0",
                'path': path,
                'username': username,
                'email': email,
                'password': password,
                'password_exp': password_exp_string,
                'twofa_code': twofa_key
            })
            
            if password != confirm_password:
                Message("The password and confirm password are not the same.", "Passwords don't match").exec_()
                return "Stop this method from further execution"
                
            payload = {
                'type': 'app', 
                'name': name, 
                'data': data,
                'group_id': group                
            }

            if self.app:
                Model().update("vault", payload, self.app[0])
            else:
                Model().save("vault", payload)
                
                
                
            self.app_update_signal.emit(True)
            self.close()
    
    def fill_data(self):
        
        self.btn_save.setText("Update")
        self.setWindowTitle("Update App")
        
        data: object = json_to_dict(self.app[3])
        
        self.lne_name.setText(data['name'])
        self.lne_password.setText(data['password'])
        self.lne_password2.setText(data['password'])
        self.lne_email.setText(data['email'])
        self.lne_username.setText(data['username'])
        self.lne_path.setText(data['path'])
        
        try:
            self.lne_twofa_code.setText(data['twofa_code'])
        except:
            pass
        
        # Get the datetime object from string
        password_exp_datetime: datetime = datetime.strptime(data['password_exp'], "%Y-%m-%d")
        
        # Get the date object from datetime object
        password_exp_date: date = date(password_exp_datetime.year, password_exp_datetime.month, password_exp_datetime.day)
        
        # Set the date
        self.dte_password_exp.setDate(password_exp_date)
        
    def add_from_desktop(self):
        file = QFileDialog.getOpenFileName(self, "Open a file", DESKTOP, "All Files (*.*)")[0]
        self.lne_path.setText(file)
        
    def update_sequence(self, index: str):
        # Get the app that needs to be updated
        update_app = list(filter(lambda a: json_to_dict(a[3])['sequence'] == index, self.secrets))[0]
        # Get the data from the app that needs to be updated
        update_app_data = json_to_dict(update_app[3])
        # The app was edited
        if self.app:
            # Get the data from the current app being updated
            data = json_to_dict(self.app[3])
            # Get the sequence to put in the app the needs to be updated
            new_sequence = data['sequence']
            update_app_data['sequence'] = new_sequence
            Model().update("vault", {'data': dumps(update_app_data)}, update_app[0])
        # It's a new app
        else:
            # its a new app
            update_app_data['sequence'] = str(len(self.secrets)+1)
            Model().update("vault", {'data': dumps(update_app_data)}, update_app[0])
            
    def show_password(self, show, field):
        if show: field.setEchoMode(QLineEdit.Normal)
        else: field.setEchoMode(QLineEdit.Password)
        
    def get_current_apps(self):
        vault_items: list[list[int, str, str, str]] = Model().read("vault")
        current_app_list = list(filter(lambda item: item[1] == "app", vault_items))
        
        current_apps: object = {}
        
        for app in current_app_list:
            current_apps[app[2]] = app
            
        return current_apps