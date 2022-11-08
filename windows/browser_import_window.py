from operator import itemgetter
import sys
import os
import json
import pandas as pd
from datetime import date, timedelta, datetime

from PyQt5.QtWidgets import (
    QDialog, 
    QTableWidgetItem, 
    QHeaderView, 
    QCheckBox, 
    QStyledItemDelegate, 
    QStyleOptionViewItem, 
    QHBoxLayout, 
    QWidget,
    QComboBox,
    QListView,
    QAbstractButton
    )
from PyQt5.QtGui import QCursor, QIcon, QFont
from PyQt5.QtCore import Qt, QModelIndex, pyqtSignal, pyqtSlot



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.browser_import_window import Ui_BrowserPasswordImportWindow

from widgetStyles.ComboBox import ComboBox
from widgetStyles.QCheckBox import CheckBoxTable
from widgetStyles.Dialog import Dialog
from widgetStyles.PushButton import PushButton
from widgetStyles.TableWidget import TableWidget
from widgetStyles.ScrollBar import ScrollBar
from widgetStyles.Widget import Widget
from widgetStyles.styles import green

from widgets.group_combobox import ComboBox as GroupComboBox

from utils.helpers import StyleSheet, set_font

from database.model import Model

from windows.groups_window import GroupsWindow


class BrowserImportWindow(Ui_BrowserPasswordImportWindow, QDialog):
    import_finished = pyqtSignal(list)
    
    def __init__(self, file) -> None:
        super(BrowserImportWindow, self).__init__()
        
        self.file = file
        self.group_dict, self.group_names = self.create_group_data()
        
        self.setupUi(self)
        self.get_file_data()
        self.read_styles()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        
        # Get the current apps to avoid collisions
        self.current_apps = self.get_current_apps()
        
        self.chk_select_all.stateChanged.connect(self.select_all)
        self.btn_import.clicked.connect(self.import_accounts)
        self.btn_groups.clicked.connect(self.manage_groups)
        
        self.chk_select_all.setChecked(True)
        
        self.corner: QAbstractButton = self.tbl_accounts.findChild(QAbstractButton)
    
    @pyqtSlot()
    def manage_groups(self) -> None:
        manage_groups_window = GroupsWindow()
        manage_groups_window.browser_import_signal.connect(self.update_groups)
        manage_groups_window.exec_()
    
    @pyqtSlot()
    def update_groups(self) -> None:
        self.group_dict, self.group_names = self.create_group_data()
        
    def create_group_data(self) -> tuple[dict, list]:
        groups = Model().read("groups")
        
        groups = sorted(groups, key=itemgetter(1))
        
        group_dict = {}
        group_names = []
        
        for group in groups:
            group_names.append(group[1])
            group_dict[group[1]] = group[0]

            
        return group_dict, group_names
        
        
    def create_checkbox(self):
        self.import_checkbox = QCheckBox()
        self.import_checkbox.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.container = QWidget()
        self.container_layout = QHBoxLayout()
        
        self.container_layout.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.import_checkbox)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container.setLayout(self.container_layout)
        
        return self.import_checkbox
    
    # Create a combo box for the groups (this method runs inside a loop that can be very long, DO NOT USE LOOP INSIDE THIS METHOD)
    def create_combobox(self):
        self.group_box = GroupComboBox()
        self.group_box.setView(QListView())
        self.group_box.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        
        widget_list = [
            self.group_box,
            self.group_box.view()
        ]

        set_font(widget_list)
        
        self.group_box.addItems(self.group_names)
            
        return self.group_box
    
    def get_checkboxes(self):
        checkbox_list = []
        number_of_items = self.tbl_accounts.rowCount()
        
        for i in range(number_of_items):
            checkbox: QCheckBox = self.tbl_accounts.cellWidget(i, 0)
            if checkbox.isChecked():
                checkbox_list.append(i)
        
        return checkbox_list
    
    def import_accounts(self):
        # Get a list of the indexes in the table that need to be imported
        item_indexes = self.get_checkboxes()
        self.import_data = []
        self.check = {}
        
        for index in item_indexes:
            name = self.tbl_accounts.item(index, 2).text()
            url = self.tbl_accounts.item(index, 3).text()
            username = self.tbl_accounts.item(index, 4).text()
            password = self.tbl_accounts.item(index, 5).text()
            
            group: QComboBox = self.tbl_accounts.cellWidget(index, 1)
            group_name = group.currentText()
            group_id = self.group_dict[group_name]
            
            # If the app with this name is already in the database or in the data meant to be imported skip this app
            if name in self.current_apps or name in self.check: continue
            # If the loop didn't continue it's a new app, add it to the check dict
            self.check[name] = name
            
            password_exp_date = date.today() + timedelta(days=90)
            password_exp_string = datetime.strftime(password_exp_date, "%Y-%m-%d")
            
            data: object = {
                'name': name,
                'sequence': "0",
                'path': url,
                'username': username,
                'email': username,
                'password': password,
                'password_exp': password_exp_string
            }
            self.import_data.append([name, json.dumps(data), group_id])
                
        self.import_finished.emit(self.import_data)
        self.close()
        
    def select_all(self, checked):
        number_of_items = self.tbl_accounts.rowCount()
        
        for i in range(number_of_items):
            checkbox: QCheckBox = self.tbl_accounts.cellWidget(i, 0)
            checkbox.setChecked(checked)
        
    def get_file_data(self):
        accounts = pd.read_csv(self.file)
        number_of_rows = len(accounts.index)
        
        self.dup_names = set()
        
        if number_of_rows < 25:
            self.setFixedHeight(200 + number_of_rows * 30)
        else:
            self.setFixedHeight(850)
        
        labels = ["Import", "Group", "Name", "URL", "Username", "Password"]
        self.tbl_accounts.setColumnCount(len(labels))
        self.tbl_accounts.setRowCount(number_of_rows)
        
        self.tbl_accounts.setHorizontalHeaderLabels(labels)
        
        header: QHeaderView = self.tbl_accounts.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        delegate = AlignDelegate(self.tbl_accounts)
        self.tbl_accounts.setItemDelegateForColumn(0, delegate)       

        for index, item in accounts.iterrows():

            checkbox = self.create_checkbox()
            group_box = self.create_combobox()

            # This is to accomodate FireFox which uses a different csv format
            name = item['name'] if "name" in item else item['httpRealm']
            self.dup_names.add(name)
            
            self.tbl_accounts.setCellWidget(index, 0, checkbox)
            self.tbl_accounts.setCellWidget(index, 1, group_box)
            self.tbl_accounts.setItem(index, 2, QTableWidgetItem(str(name)))
            self.tbl_accounts.setItem(index, 3, QTableWidgetItem(str(item['url'])))
            self.tbl_accounts.setItem(index, 4, QTableWidgetItem(str(item['username'])))
            self.tbl_accounts.setItem(index, 5, QTableWidgetItem(str(item['password'])))
            
    def read_styles(self):
        widget_list = [
            Dialog,
            Widget,
            ScrollBar,
            TableWidget,
            PushButton,
            ComboBox,
            CheckBoxTable,
        ]
        stylesheet = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)
        
        font_list = [
            self.label,
            self.btn_import,
            self.chk_select_all,
            self.tbl_accounts,
            self.tbl_accounts.horizontalHeader(),
            self.tbl_accounts.verticalHeader(),
            self.btn_groups
            
        ]
        set_font(font_list)
    
    def get_current_apps(self):
        vault_items: list[list[int, str, str, str]] = Model().read("vault")
        current_app_list = list(filter(lambda item: item[1] == "app", vault_items))
        
        current_apps: object = {}
        
        for app in current_app_list:
            current_apps[app[2]] = app
            
        return current_apps
        
class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter