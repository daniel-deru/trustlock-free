from operator import itemgetter
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QDialog, QFileDialog, QLineEdit, QWidget
from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot, QSize
from PyQt5.QtGui import QFont, QIcon, QCloseEvent

from designs.python.groups_window import Ui_GroupsWindow

from database.model import Model

from windows.group_window import GroupWindow

from widgets.group_widget import GroupWidget

from utils.helpers import StyleSheet, set_font, clear_window

from widgetStyles.Label import Label
from widgetStyles.PushButton import PushButton
from widgetStyles.Dialog import Dialog
from widgetStyles.ScrollArea import ScrollAreaGroups
from widgetStyles.ScrollBar import ScrollBarGroups

class GroupsWindow(Ui_GroupsWindow, QDialog):
    browser_import_signal: pyqtSignal = pyqtSignal(bool)
    
    def __init__(self) -> None:
        super(GroupsWindow, self).__init__()
        self.groups = sorted(Model().read("groups"), key=itemgetter(1))
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))

        self.set_groups()
        self.read_styles()
        

        self.btn_add_group.clicked.connect(self.add_group)
    
    def set_window_height(self, num_groups):
        min_height = 130
        max_height = 600        
        height = min_height + (55 * num_groups)
        
        if(num_groups < 10):
            self.setFixedHeight(height)
        else:
            self.setFixedHeight(max_height)
            
    def read_styles(self):
        widget_list = [
            ScrollAreaGroups, 
            Dialog, 
            PushButton, 
            Label,
            ScrollBarGroups
        ]
        
        stylesheet = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)
        
        font_list = [
            self.lbl_groups,
            self.btn_add_group
        ]
        set_font(font_list)
        
    def add_group(self):
        manage_group_window = GroupWindow()
        manage_group_window.group_add_signal.connect(self.update_window)
        manage_group_window.exec_()
        
    def set_groups(self):
        # Empty the container if their are any remaining widgets
        clear_window(self.vbox_group_container)
        # Get the initial group data   
        group_data = self.get_group_data()
        self.set_window_height(len(list(group_data.keys())))
        
        # Create the GroupWidget and add it to the UI
        for group_id in group_data:
            
            group_widget = GroupWidget(group_data[group_id])
            group_widget.group_delete_signal.connect(self.update_window)
            group_widget.group_update_signal.connect(self.update_window)
            self.vbox_group_container.addWidget(group_widget)
            
    @pyqtSlot()
    def update_window(self):
        self.set_groups()
            
    @pyqtSlot(int)
    def delete_group(self, id) -> None:
        # Delete the group
        Model().delete("groups", id)
        # Update the UI
        self.set_groups()
            
    def get_group_data(self):
        # Create the initial group dict with all the current groups
        groups = Model().read('groups')
        groups = sorted(groups, key=itemgetter(1))
        group_dict = {}
        
        for group in groups:
            group_dict[str(group[0])] = {
                'id': group[0],
                'name': group[1], 
                'description': group[2], 
                'data': {}
            }
        
        # Get all the features
        apps = Model().read("apps") # 4 index of group_id
        vault = Model().read("vault") # 4 index of group_id
        notes = Model().read("notes") # 3 index of group_id
        todos = Model().read("todos") # 5 index of group_id
        
        features = {
            'apps': [apps, 4],
            'vault': [vault, 4],
            'notes': [notes, 3],
            'todos': [todos, 5]
        }
        
        # Add the features to the group dict
        self.create_feature_groups('apps', features['apps'], group_dict)
        self.create_feature_groups('vault', features['vault'], group_dict)
        self.create_feature_groups('notes', features['notes'], group_dict)
        self.create_feature_groups('todos', features['todos'], group_dict)
  
        return group_dict
        
        
    def create_feature_groups(self, name, data, group_dict):
        feature_items, group_id_index = data
        for group_id in group_dict:
            group_dict[group_id]['data'][name] = 0
        
        for feature in feature_items:
            group_id = feature[group_id_index]
            if group_id not in group_dict:
                break
            if name in group_dict[group_id]['data']:
                group_dict[group_id]['data'][name] += 1
                
    def closeEvent(self, event: QCloseEvent) -> None:
        self.browser_import_signal.emit(True)
        return super().closeEvent(event)
        