from operator import itemgetter
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QDialog, QFileDialog, QListView
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QFont


from utils.helpers import StyleSheet, set_font
from utils.message import Message
from widgetStyles.PushButton import PushButton
from widgetStyles.LineEdit import LineEdit
from widgetStyles.SpinBox import SpinBox
from widgetStyles.Dialog import Dialog
from widgetStyles.Label import Label
from widgetStyles.ComboBox import ComboBox
from database.model import Model

from designs.python.apps_edit_window import Ui_AppsEdit

DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE'], 'Desktop'))

class AppsEdit(Ui_AppsEdit, QDialog):
    app_edit_window_signal = pyqtSignal(str)
    def __init__(self, app):
        super(AppsEdit, self).__init__()
        self.app = app
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.cmb_group.setView(QListView())
        self.cmb_group.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.read_styles()
        self.fill_fields()
        
        self.apps = Model().read("apps")

        self.spnbox_index.setValue(len(self.apps))
        self.spnbox_index.setMaximum(len(self.apps))
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
            Label,
            ComboBox
        ]

        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        
        font_widgets = [
            self.lbl_index,
            self.lbl_name,
            self.lbl_path,
            self.lnedt_name,
            self.lnedt_path,
            self.spnbox_index,
            self.btn_desktop,
            self.btn_discard,
            self.btn_save,
            self.lbl_group,
            self.cmb_group,
            self.cmb_group.view()
        ]
        
        set_font(font_widgets)
    
    def fill_fields(self):
        
        groups = Model().read("groups")
        
        groups = sorted(groups, key=itemgetter(1))
        
        current_group = 0
            
        for i in range(len(groups)):
            if int(self.app[4]) == groups[i][0]:
                current_group = i
            self.cmb_group.addItem(groups[i][1], groups[i][0])

        self.cmb_group.setCurrentIndex(current_group) 
        self.lnedt_name.setText(self.app[1])
        self.lnedt_path.setText(self.app[2])
        self.spnbox_index.setValue(int(self.app[3]))


    def add_from_desktop(self):
        file = QFileDialog.getOpenFileName(self, "Open a file", DESKTOP, "All Files (*.*)")[0]
        path = self.lnedt_path
        path.setText(file)


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
            Message("Please enter a name for your app", "No name").exec_()
            return
        elif not path:
            Message("Please enter a path for your app", "No path").exec_()
            return
        else:
            
            if self.app is not None:
                Model().update('apps', data, self.app[0])
                self.app_edit_window_signal.emit("updated")
            self.close()

    
