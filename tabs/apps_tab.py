from operator import itemgetter
import sys
import os
import math

from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


from designs.python.apps_tab import Ui_apps_tab
from database.model import Model

from windows.apps_window import Apps_window
from windows.delete import DeleteWindow

from widgets.app_item import AppItem
from widgets.filter_group_widget import FilterGroupWidget

from widgetStyles.PushButton import PushButton
from widgetStyles.QCheckBox import CheckBoxSquare
from widgetStyles.Line import Line
from widgetStyles.ScrollBar import ScrollBar

from utils.helpers import StyleSheet, clear_window, set_font
from utils.message import Message

class Apps_tab(Ui_apps_tab, QWidget):
    app_signal = pyqtSignal(str)
    table_signal = pyqtSignal(str)

    def __init__(self):
        super(Apps_tab, self).__init__()
        self.setupUi(self)
        
        self.filter_widget = FilterGroupWidget()
        self.filter_widget.group_changed_signal.connect(lambda group: self.create_apps(group))
        self.hbox_filter_widget.addWidget(self.filter_widget)
        
        initial_group = self.filter_widget.get_current_group()
        self.create_apps(initial_group)
        
        self.read_styles()

        self.btn_add_app.clicked.connect(self.add_app)
        
        self.btn_delete.clicked.connect(self.delete)
        
        # Signal slots for external signals
        self.app_signal.connect(self.update)
        # Login signal will run everytime the login signal is updated
        
    def delete(self):
        delete_window = DeleteWindow('apps')
        delete_window.delete_signal.connect(self.update)
        delete_window.exec_()
    
    def create_tab(self):
        return self

    def read_styles(self):
        styles = [
            CheckBoxSquare, 
            PushButton, 
            Line,
            ScrollBar
        ]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        
        widget_list = [
            self.btn_add_app,
            self.lbl_open_apps,
            self.btn_delete
        ]
        
        set_font(widget_list)

    def add_app(self):
        app_window = Apps_window()
        app_window.app_window_signal.connect(self.update)
        app_window.exec_()
    
    def create_apps(self, group):
        clear_window(self.gbox_apps)
        apps = Model().read('apps')
        
        apps = sorted(apps, key=itemgetter(1))
        
        current_group = list(filter(lambda app: app[4] == str(group), apps))
        COLUMNS = 4
        grid_items = []
        for i in range(math.ceil(len(current_group)/COLUMNS)):
            subarr = []
            for j in range(COLUMNS):
                if current_group:
                    subarr.append(current_group.pop(0))
            grid_items.append(subarr)
            
        for i in range(len(grid_items)):
            row = i
            for j in range(len(grid_items[i])):
                col = j
                app_button = AppItem(grid_items[i][j]).create()
                app_button.app_clicked_signal.connect(self.get_app)
                self.gbox_apps.addWidget(app_button, row, col)
  
    # Handles the editing of the apps
    def get_app(self, app):
        
        open_or_edit = Message("Do you want to open or edit the app?", "Open Or Edit?").prompt(('Open', 'Edit'))
        should_open = open_or_edit == QMessageBox.Yes
        
        if not should_open:
            app_window = Apps_window(app)
            app_window.app_window_signal.connect(self.update)
            app_window.exec_()
        else:
            try:
                os.startfile(app[2])
            except OSError:
                pass

    def update(self):
        clear_window(self.gbox_apps)
        initial_group = self.filter_widget.get_current_group()
        self.create_apps(initial_group)
        self.read_styles()