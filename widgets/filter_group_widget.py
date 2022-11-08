from operator import itemgetter
import sys
import os
from tkinter.ttk import Style
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import time

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QComboBox, QListView
from PyQt5.QtGui import QCursor, QFont, QMouseEvent
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt

from database.model import Model

from windows.groups_window import GroupsWindow

from utils.helpers import set_font, StyleSheet

from widgetStyles.ComboBox import ComboBoxFilter

class FilterGroupWidget(QWidget):
    group_changed_signal = pyqtSignal(int)
    
    def __init__(self) -> None:
        super(FilterGroupWidget, self).__init__()
        self.setupUi()
        self.show_groups()
        self.read_styles()        
        
        self.btn_manage_groups.clicked.connect(self.manage_groups)
        
        self.cmb_groups.currentIndexChanged.connect(self.filter)
        
    def read_styles(self):
        style_list = [ComboBoxFilter]
        stylesheet = StyleSheet(style_list).create()
        self.setStyleSheet(stylesheet)
        
    @pyqtSlot()
    def filter(self):
        groups = Model().read("groups")
        current_text = self.cmb_groups.currentText()
        for group in groups:
            if group[1] != current_text:
                continue
            else:
                self.group_changed_signal.emit(group[0])
                break
    
    @pyqtSlot()  
    def manage_groups(self):
        manage_groups_window = GroupsWindow()
        manage_groups_window.exec_()
        
    def setupUi(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        
        self.cmb_groups = ComboBox()
        self.cmb_groups.setView(QListView())
        self.cmb_groups.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        
        self.btn_manage_groups = QPushButton("Edit Groups")
        self.btn_manage_groups.setCursor(QCursor(Qt.PointingHandCursor))
        
        hbox.addWidget(self.cmb_groups)
        hbox.addWidget(self.btn_manage_groups)
        
        self.setLayout(hbox)
        
        font_list = [
            self.cmb_groups, 
            self.btn_manage_groups,
            self.cmb_groups.view()
        ]
        set_font(font_list)
        
    def show_groups(self):
        self.cmb_groups.clear()
        groups = Model().read("groups")
        
        groups = sorted(groups, key=itemgetter(1))
        
        for group in groups:
            self.cmb_groups.addItem(group[1], group[0])
            
        for i in range(len(groups)):
            if groups[i][1] == "Ungrouped":
                self.cmb_groups.setCurrentIndex(i)
            
    def get_current_group(self):
        # Update the UI when the update function is called in the tabs
        self.read_styles()
        groups = Model().read("groups")
        for group in groups:
            if group[1] != self.cmb_groups.currentText():
                continue
            else:
                return group[0]
    

# Custom Combobox implementation to update the class everytime the user opens the combobox
class ComboBox(QComboBox):
    current_index: int
    def showPopup(self) -> None:
        # Store the current index since it will be removed by "self.clear()"
        self.current_index = self.currentIndex()
        # Clear the old data
        self.clear()
        # Get the new groups from the database
        groups = Model().read("groups")
        
        groups = sorted(groups, key=itemgetter(1))
        # Add the groups to the combobox
        group_list = []
        for group in groups:
            group_list.append(group[1])

        self.addItems(group_list)
        # Set the original index back
        self.setCurrentIndex(self.current_index)
        # Call the parent method
        super(ComboBox, self).showPopup()
            
    