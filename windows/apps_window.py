from operator import itemgetter
import sys
import os
from PyQt5.QtWidgets import QDialog, QFileDialog, QListView
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.app_window import Ui_App_Window
from database.model import Model
from utils.message import Message
from utils.helpers import StyleSheet, set_font

from windows.group_window import GroupWindow

from widgetStyles.Dialog import Dialog
from widgetStyles.LineEdit import LineEdit
from widgetStyles.PushButton import PushButton, IconToolButton
from widgetStyles.Label import Label
from widgetStyles.SpinBox import SpinBox
from widgetStyles.QCheckBox import SettingsCheckBox
from widgetStyles.ComboBox import ComboBox

DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE'], 'Desktop'))

class Apps_window(Ui_App_Window, QDialog):
    app_window_signal = pyqtSignal(str)
    def __init__(self, app=None):
        super(Apps_window, self).__init__()
        self.setupUi(self)
        self.show_groups()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.setWindowTitle("Add Your App")
        self.read_styles()
        
        self.app = app
        self.apps = Model().read('apps')
        
        self.fill_data()

        self.btn_save.clicked.connect(self.save_clicked)
        self.tbtn_desktop.clicked.connect(self.add_from_desktop)
        self.btn_discard.clicked.connect(lambda: self.close())
        self.tbtn_add.clicked.connect(self.add_new_group)
        
    def add_new_group(self):
        group_window = GroupWindow()
        group_window.group_add_signal.connect(lambda: self.show_groups())
        group_window.exec_()
        
    def show_groups(self):
        groups = Model().read("groups")
        self.cmb_group.clear()
        
        groups = sorted(groups, key=itemgetter(1))
        
        for i in range(len(groups)):
            if groups[i][1] == "Ungrouped":
                self.cmb_group.setCurrentIndex(i)
            self.cmb_group.addItem(groups[i][1], groups[i][0])
        
        for i in range(len(groups)):
            if groups[i][1] == "Ungrouped":
                self.cmb_group.setCurrentIndex(i)
        

    def save_clicked(self):
        
        name = self.lnedt_name.text()
        path = self.lnedt_path.text()
        group = self.cmb_group.currentData()

        data = {
                    'name': name,
                    'path': path,
                    'sequence': '0',
                    'group_id': group
                }
        
        if not name:
           return Message("Please enter a name for your app", "No name").exec_()
        elif not path:
           return Message("Please enter a path for your app", "No path").exec_()
        self.save_apps(data)
    
    def save_apps(self, data):

        if(not self.app):
            for app in self.apps:
                if data['name'] in app:
                    return Message("This name is already being used", "Name already exists").exec_()
            Model().save('apps', data)
        else:
            Model().update('apps', data, self.app[0])

        self.app_window_signal.emit("saved")
        self.close()

    def add_from_desktop(self):
        file = QFileDialog.getOpenFileName(self, "Open a file", DESKTOP, "All Files (*.*)")[0]
        path = self.lnedt_path
        path.setText(file)

    def read_styles(self):
        self.cmb_group.setView(QListView())
        self.cmb_group.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        
        styles = [
            Dialog,
            LineEdit,
            PushButton,
            Label,
            SpinBox,
            SettingsCheckBox,
            ComboBox,
            IconToolButton()
        ]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        
        font_list = [
            self.btn_save,
            self.tbtn_desktop,
            self.btn_discard,
            self.lbl_name,
            self.lbl_path,
            self.lnedt_name,
            self.lnedt_path,
            self.lbl_group,
            self.cmb_group,
            self.cmb_group.view(),
            self.tbtn_add
        ]
        
        set_font(font_list)
        
        self.tbtn_desktop.setIcon(QIcon(":/button_icons/file_white"))
        
    def fill_data(self):
        if(not self.app):
            return
        
        groups = Model().read("groups")
        
        groups = sorted(groups, key=itemgetter(1))
        
        current_group = 0
        self.cmb_group.clear()
            
        for i in range(len(groups)):
            if int(self.app[4]) == groups[i][0]:
                current_group = i
            self.cmb_group.addItem(groups[i][1], groups[i][0])

        self.cmb_group.setCurrentIndex(current_group) 
        self.lnedt_name.setText(self.app[1])
        self.lnedt_path.setText(self.app[2])