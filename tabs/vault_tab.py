from operator import itemgetter
import os
import re
import sys
import json
import math

from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QResizeEvent, QIcon


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.vault_tab import Ui_Vault_tab

from utils.helpers import StyleSheet, clear_window, set_font

from widgets.vault_item import VaultItem
from widgets.filter_group_widget import FilterGroupWidget

from windows.secret_window import SecretWindow
from windows.crypto_vault_window import CryptoVaultWindow
from windows.app_vault_window import AppVaultWindow
from windows.vault_type_window import VaultType
from windows.app_vault_view_window import AppVaultView
from windows.crypto_vault_view_window import CryptoVaultViewWindow
from windows.general_vault_view_window import GeneralVaultView
from windows.delete import DeleteWindow
from windows.login_window import Login

from widgetStyles.QCheckBox import CheckBoxSquare
from widgetStyles.PushButton import PushButton
from widgetStyles.Label import Label
from widgetStyles.LineEdit import LineEditSearch
from widgetStyles.ScrollBar import ScrollBar

from database.model import Model

class Vault_tab(Ui_Vault_tab, QWidget):
    vault_signal = pyqtSignal(str)
    login_signal = pyqtSignal(str)
    logout_signal = pyqtSignal(bool)
    
    def __init__(self):
        super(Vault_tab, self).__init__()
        self.setupUi(self)
        self.COLUMNS = 3
        self.filter_widget = FilterGroupWidget()
        self.filter_widget.group_changed_signal.connect(lambda group: self.update_by_group(group))
        self.hbox_filter_widget.addWidget(self.filter_widget)
        self.read_styles()
        
        initial_group = self.filter_widget.get_current_group()
        self.update_by_group(initial_group)

        self.btn_add.clicked.connect(self.add_clicked)
        self.btn_delete.clicked.connect(self.delete_secret)
        self.btn_search.clicked.connect(self.search_items)
        self.btn_lock.clicked.connect(lambda: self.logout_signal.emit(True))
       
        self.vault_signal.connect(self.update)

        self.logged_in = False
        
    def vault_login(self, secret):
        login_window = Login(update_password=True)
        login_window.update_password_status.connect(lambda status: self.open_secret(secret, status))
        login_window.exec_()
        
    def search_items(self):
        search_for = self.lne_search.text()
        current_group = self.filter_widget.get_current_group()
        
        group_items = self.get_group_items(current_group)
        
        found_items = []

        for group in group_items:
            item_list = []
            for item in group:
                if(re.match(f".*{search_for}.*", item[2], re.IGNORECASE)):
                    item_list.append(item)
            if(len(item_list) > 0):
                found_items.append(item_list)
                
        self.create_secrets(found_items)
        

    def create_tab(self):
        return self

    def read_styles(self):
        styles = [
            PushButton,
            CheckBoxSquare,
            Label,
            ScrollBar,
            LineEditSearch
        ]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)

        widget_list = [
            self.btn_add,
            self.lbl_secret,
            self.btn_delete,
            self.btn_search,
            self.lne_search,
            self.btn_lock
        ]

        set_font(widget_list)

    def add_clicked(self):
        vault_type = VaultType()
        vault_type.vault_type_signal.connect(self.open_vault)
        vault_type.exec_()

    
    def open_vault(self, signal):
        if(signal == "general"):
            new_secret = SecretWindow()
            new_secret.secret_signal.connect(self.update)
            new_secret.exec_()
        elif signal == "app":
            app_secret = AppVaultWindow()
            app_secret.app_update_signal.connect(self.update)
            app_secret.exec_()
        elif signal == "crypto":
            new_crypto_secret = CryptoVaultWindow()
            new_crypto_secret.crypto_update_signal.connect(self.update)
            new_crypto_secret.exec_()
    
    def update_by_group(self, group):
        grid_items = self.get_group_items(group)
        self.create_secrets(grid_items)

            
    def get_group_items(self, group) -> list:
        secrets = Model().read('vault')
        
        secrets = sorted(secrets, key=itemgetter(2))
        
        current_group = list(filter(lambda todo: todo[4] == str(group), secrets))
       
        # Create the nested list for the grid layout
        grid_items = []
             
        for i in range(math.ceil(len(current_group)/self.COLUMNS)):
            subarr = []
            for j in range(self.COLUMNS):
                if current_group:
                    subarr.append(current_group.pop(0))
            grid_items.append(subarr)
            
        return grid_items
    
    def create_secrets(self, grid_items):
        clear_window(self.gbox_secrets)
        # Loop over the nested list and add items to the grid layout
        for i in range(len(grid_items)):
            for j in range(len(grid_items[i])):
                self.btn_vault = VaultItem(grid_items[i][j]).create()
                self.btn_vault.vault_clicked_signal.connect(self.open_secret)
                self.gbox_secrets.addWidget(self.btn_vault, i, j)

    
    # Clear the window from the data add the data back and read the styles
    def update(self):
        clear_window(self.gbox_secrets) # clear the grid before adding new items
        
        # Get the current group index
        initial_group = self.filter_widget.get_current_group()
        self.update_by_group(initial_group)
        self.read_styles()
            
    
    def app_vault_click(self, secret):
        data = json.loads(secret[3])
        try:
            os.startfile(data['path'])
        except OSError:
            pass

    def delete_secret(self):
        delete_window = DeleteWindow('vault')
        delete_window.delete_signal.connect(self.update)
        delete_window.exec_()
    
    def open_secret(self, secret: tuple):
        if secret[1] == "app":
            app_view = AppVaultView(secret)
            app_view.update_signal.connect(self.update)
            app_view.exec_()
        elif secret[1] == "crypto":
            crypto_vault = CryptoVaultViewWindow(secret)
            crypto_vault.update_signal.connect(self.update)
            crypto_vault.exec_()
        elif secret[1] == "general":
            general_vault = GeneralVaultView(secret)
            general_vault.update_signal.connect(self.update)
            general_vault.exec_()
