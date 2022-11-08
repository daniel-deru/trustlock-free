from operator import itemgetter
import os
import sys
from turtle import clear
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QDialog, QListView, QCheckBox, QWidget
from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot
from PyQt5.QtGui import QIcon, QFont, QCursor

from database.model import Model

from widgetStyles.ComboBox import ComboBox
from widgetStyles.PushButton import PushButton
from widgetStyles.Label import Label, LabelLarge
from widgetStyles.QCheckBox import CheckBox
from widgetStyles.Dialog import Dialog
from widgetStyles.ScrollArea import ScrollArrea
from widgetStyles.ScrollBar import ScrollBar

from utils.helpers import StyleSheet, set_font, clear_window

from designs.python.delete_window import Ui_DeleteWindow

group_id_index = {
    'apps': 4,
    'vault': 4,
    'notes': 3,
    'todos': 5
}

class DeleteWindow(Ui_DeleteWindow, QDialog):
    delete_signal = pyqtSignal(bool)
    
    def __init__(self, function) -> None:
        super(DeleteWindow, self).__init__()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.setupUi(self)
        self.cmb_groups.setView(QListView())
        self.cmb_groups.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.set_style()
        
        self.font_name = Model().read('settings')[0][2]
        # Create empty class variable for the current items
        self.current_items = None

        self.function = function
        self.function_items = Model().read(function)
        
        getter_index = 2 if function == "vault" else 1
        self.function_items = sorted(self.function_items, key=itemgetter(getter_index))
        
        self.groups = sorted(Model().read("groups"), key=itemgetter(1))
        
        # Set the current items
        self.set_data()
        
        self.cmb_groups.currentIndexChanged.connect(self.set_items)
        self.chk_select_all.stateChanged.connect(self.select_all)
        
        self.btn_discard.clicked.connect(self.close)
        self.btn_delete.clicked.connect(self.delete_items)
        
    @pyqtSlot()
    def delete_items(self):
        item_container = self.vbox_items
        
        # get the checkbox, see if it is checked and delete the item if it is checked
        for i in range(item_container.count()):
            checkbox: QCheckBox = item_container.itemAt(i).widget()
            if checkbox.isChecked():
                name = checkbox.text()
                id = self.current_items[name]
                Model().delete(self.function, id)
        
        # Send update signal to update the window
        self.delete_signal.emit(True)
        self.close()
                
            
        
    def set_data(self):
        # Set the groups
        for group in self.groups:
            self.cmb_groups.addItem(group[1], group[0])
            
        for i in range(len(self.groups)):
            if self.groups[i][1] == "Ungrouped":
                self.cmb_groups.setCurrentIndex(i)
            
        # Set function name
        self.lbl_function.setText(self.function)
        
        # Set the items
        self.set_items()
        
    def get_current_group_items(self):
        current_group = self.cmb_groups.currentData()
        
        # Get the items for the current group
        current_items_full = list(filter(lambda item: item[group_id_index[self.function]] == str(current_group), self.function_items))
        item_dict = {}
        # Get the index of the name field based on the table
        name_index = 1 if self.function != 'vault' else 2
        # Get the name and id from the current items
        for item in current_items_full:
            item_dict[item[name_index]] = item[0]
        
        return item_dict
    
    def set_items(self):
        clear_window(self.vbox_items)
        current_items = self.get_current_group_items()
        
        for name in current_items:
            checkbox = QCheckBox(name)
            checkbox.setFont(QFont(self.font_name))
            checkbox.setCursor(QCursor(Qt.PointingHandCursor))
            self.vbox_items.addWidget(checkbox)
        
        # Set the current items as a class variable
        self.current_items = current_items
    
    # @pyqtSlot(int)
    def select_all(self, checked):
        num_checkboxes = self.vbox_items.count()
        
        for i in range(num_checkboxes):
            checkbox = self.vbox_items.itemAt(i).widget()
            checkbox.setChecked(checked)
                   
    def set_style(self):
        style_list = [
            Label,
            Dialog,
            PushButton,
            CheckBox,
            ComboBox,
            LabelLarge("#lbl_function"),
            ScrollArrea,
            ScrollBar
        ]
        
        stylesheet = StyleSheet(style_list).create()
        self.setStyleSheet(stylesheet)
        
        widget_list = [
            self.lbl_function,
            self.lbl_select_group,
            self.btn_delete,
            self.btn_discard,
            self.cmb_groups,
            self.cmb_groups.view(),
            self.chk_select_all
        ]
        set_font(widget_list)
    
        