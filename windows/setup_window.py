import sys
import os
import json

from PyQt5.QtWidgets import (QDialog)
from PyQt5.QtGui import QCursor, QIcon, QCloseEvent, QFont
from PyQt5.QtCore import Qt, pyqtSignal, QSize


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.setup_window import Ui_InitialSetup

from database.model import Model

from windows.twofa_window import TwofaDialog
from windows.timer_window import Timer

from utils.globals import DESKTOP
from utils.helpers import StyleSheet, set_font

from widgets.setup_widget import SetupWidget

from widgetStyles.PushButton import PushButton, PushButton100Width, ButtonBackIcon
from widgetStyles.Label import Label
from widgetStyles.Dialog import Dialog

class InitialSetup(Ui_InitialSetup, QDialog):
    setup_finished = pyqtSignal(bool)
    def __init__(self) -> None:
        super(InitialSetup, self).__init__()
        self.setupUi(self)
        self.setFixedHeight(200)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        
        self.auto_save_google = False
        self.auto_save_onedrive = False
        
        # This list will be passed to the StackedWidget Item to show the message and run the respective function
        self.setup_list = [
            ["Do you want to use Two Factor Authentication?", "https://smartmetatec.com", self.setup_twofa],
            ["Do you want to turn on dark mode?", "https://smartmetatec.com", self.setup_night_mode],
            ["Set the login timer duration.", "https://smartmetatec.com", self.setup_login_timer]
        ]
        self.lbl_setup.setText(f"Step {self.stack_widget.currentIndex()+2} of {len(self.setup_list)}")
        self.create_stack()
        self.read_styles()
        
        self.btn_back.clicked.connect(self.prev_widget)
        
    def read_styles(self):
        widget_list = [
            PushButton100Width,
            Label,
            Dialog
        ]
        
        stylesheet = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)
        
        self.lbl_setup.setStyleSheet("font-size: 20px;font-weight: bold;")
        self.btn_back.setIcon(QIcon(":/button_icons/back"))
        self.btn_back.setStyleSheet(ButtonBackIcon)
        self.btn_back.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_back.setIconSize(QSize(40, 40))
        
        set_font([self.lbl_setup])
    
    def create_stack(self):        
        for i in range(len(self.setup_list)):
            step_string = f"Step {i+1} of {len(self.setup_list)}"
            widget_instance = SetupWidget([*self.setup_list[i], step_string])
            widget_instance.next_signal.connect(self.next_widget)
            widget = widget_instance.create_widget()
            self.stack_widget.addWidget(widget)
            
    def next_widget(self):
        current_index = self.stack_widget.currentIndex()
        
        if current_index >= len(self.setup_list) - 1:
            self.close()
        self.stack_widget.setCurrentIndex(current_index + 1)
        self.lbl_setup.setText(f"Step {self.stack_widget.currentIndex()+1} of {len(self.setup_list)}")
    
    def prev_widget(self):
        current_index = self.stack_widget.currentIndex()
        self.stack_widget.setCurrentIndex(current_index - 1)
        self.lbl_setup.setText(f"Step {self.stack_widget.currentIndex()+1} of {len(self.setup_list)}")
        
    def setup_login_timer(self):
        timer_window = Timer()
        timer_window.exec_()
            
              
    def setup_twofa(self):
        Model().update("settings", {'twofa': '1'}, 'settings')
        twofa_window = TwofaDialog()
        twofa_window.exec_()
        
    def setup_night_mode(self):
        Model().update("settings", {'nightmode': "1"}, 'settings')
        
        
    def closeEvent(self, event: QCloseEvent) -> None:
        self.setup_finished.emit(True)
        auto_save = {
            "google": False,
            "onedrive": False
        }
        
        if self.auto_save_google: auto_save['google'] = True      
        if self.auto_save_onedrive: auto_save['onedrive'] = True

        Model().update('settings', {'auto_save': json.dumps(auto_save)}, 'settings')

        return super().closeEvent(event)
    
    def updateWindow(self):
        pass
            
    
        
    