import os
import sys

from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.protected_apps_edit_window import Ui_ProtectedAppsEdit
from utils.helpers import StyleSheet
from utils.message import Message
import assets.resources
from widgetStyles.PushButton import PushButton
from widgetStyles.LineEdit import LineEdit
from widgetStyles.SpinBox import SpinBox
from widgetStyles.Dialog import Dialog
from widgetStyles.Label import Label
from database.model import Model

DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE'], 'Desktop'))

class ProtectedApps(QDialog, Ui_ProtectedAppsEdit):
    protected_app_window_signal = pyqtSignal(str)
    def __init__(self, app):
        super(ProtectedApps, self).__init__()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.app = app
        self.setupUi(self)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.read_styles()
        self.fill_fields()
        self.protected_apps = Model().read('protected_apps')

        self.spnbox_index.setValue(len(self.protected_apps))
        self.spnbox_index.setMaximum(len(self.protected_apps))
        self.spnbox_index.setMinimum(1)

        
        self.btn_discard.clicked.connect(lambda: self.close())
        self.btn_desktop.clicked.connect(self.add_from_desktop)
        self.btn_save.clicked.connect(self.save_clicked)
        
    def read_styles(self):
        styles = [
            PushButton,
            LineEdit,
            SpinBox,
            Dialog,
            Label
        ]

        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
    
    def fill_fields(self):
        name = self.lnedt_name
        path = self.lnedt_path
        sequence = self.spnbox_index
        username = self.lnedt_username
        email = self.lnedt_email
        password = self.lnedt_password

        name.setText(self.app[1])
        path.setText(self.app[2])
        sequence.setValue(self.app[3])
        username.setText(self.app[4])
        email.setText(self.app[5])
        password.setText(self.app[6])

    def add_from_desktop(self):
        file = QFileDialog.getOpenFileName(self, "Open a file", DESKTOP, "All Files (*.*)")[0]
        path = self.lnedt_path
        path.setText(file)
    
    def save_clicked(self):
        name = self.lnedt_name.text()
        path = self.lnedt_path.text()
        sequence = self.spnbox_index.value()
        username = self.lnedt_username.text()
        email = self.lnedt_email.text()
        password = self.lnedt_password.text()

        

        data = {
                    'name': name,
                    'path': path,
                    'sequence': sequence,
                    'username': username,
                    'email': email,
                    'password': password
                }
            

        if not name:
            Message("Please enter a name for your app", "No name").exec_()
            return
        elif not path:
            Message("Please enter a path for your app", "No path").exec_()
            return
        elif not password:
            Message("Please enter the password used by the protected app", "Password Required").exec_()
            return
        elif not username and not email:
            Message("You must provide either a username or an email that is used by the protected app", "Missing field").exec_()
            return
        else:
            
            if self.app is not None:
                if self.app[3] != sequence:
                    old = self.app[3] - 1
                    new = sequence - 1
                    move_up = True if old > new else False
                    global array
                    if move_up:
                        array = self.protected_apps[new:old]
                    elif not move_up:
                        array = self.protected_apps[old+1:new+1]
                    for app in array:
                        app = list(app)
                        if move_up:
                            Model().update('protected_apps', {'sequence': app[3] + 1}, app[0])
                        elif not move_up:
                            Model().update('protected_apps', {'sequence': app[3] - 1}, app[0])
                Model().update('protected_apps', data, self.app[0])
                self.protected_app_window_signal.emit("updated")
            self.close()

