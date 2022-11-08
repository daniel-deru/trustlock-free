import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QIcon, QCursor

from designs.python.register_window import Ui_Register

from tabs.new_user_tab import NewUserTab
from tabs.existing_user_tab import ExistingUserTab

from utils.helpers import set_font, StyleSheet
from utils.enums import RegisterStatus

from widgetStyles.Dialog import Dialog
from widgetStyles.Label import Label, LabelWhite
from widgetStyles.Widget import SideWidget
from widgetStyles.PushButton import PushButton, IconToolButton
from widgetStyles.LineEdit import LineEdit
from widgetStyles.QCheckBox import BlackEyeCheckBox
from widgetStyles.Calendar import Calendar
from widgetStyles.DateEdit import DateEditForm
from widgetStyles.TabBar import RegisterTabBar



class Register(Ui_Register, QDialog):
    register_close_signal: pyqtSignal = pyqtSignal(RegisterStatus)
    def __init__(self) -> None:
        super(Register, self).__init__()
        self.setupUi(self)
        
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        
        pixmap = QPixmap(":/other/SMT Logo.png")
        app_logo_pixmap = QPixmap(":/other/app_logo")
        app_logo_pixmap = app_logo_pixmap.scaledToWidth(200)
        self.lbl_company.setPixmap(pixmap)
        self.lbl_workmate_logo.setPixmap(app_logo_pixmap)
        
        self.tab_widget_start.tabBar().setCursor(QCursor(Qt.PointingHandCursor))
        
        self.registered = False
        
        self.add_tabs()
        self.set_style()
        
    def add_tabs(self):
        new_user_tab = NewUserTab().create_tab()
        new_user_tab.register_close_signal.connect(self.register_handler)
        self.tab_widget_start.addTab(new_user_tab, "New User")
        
        existing_user_tab = ExistingUserTab().create_tab()
        existing_user_tab.existing_user_signal.connect(self.register_handler)
        self.tab_widget_start.addTab(existing_user_tab, "Existing User")
        
    def register_handler(self, signal):
        if(signal == RegisterStatus.user_created):
            self.registered = True
            self.hide()
            self.close()
        
    def set_style(self):
        style_list = [
            PushButton,
            LabelWhite,
            LineEdit,
            Dialog,
            SideWidget,
            BlackEyeCheckBox,
            DateEditForm,
            Calendar,
            IconToolButton(),
            RegisterTabBar
        ]
        
        stylesheet = StyleSheet(style_list).create()
        self.setStyleSheet(stylesheet)
        
        self.lbl_create_account.setStyleSheet("color: white;margin-top: 30px;font-size: 20px;font-weight: 700;height: 200px;")
        self.lbl_developed_by.setStyleSheet("color: white;")
        
        widget_list = [
            self.lbl_developed_by,
            self.lbl_company,
            self.lbl_create_account,
            self.lbl_workmate_logo,
            self.tab_widget_start
        ]
        
        set_font(widget_list)
        
    def closeEvent(self, event):
        if not self.registered:
            self.register_close_signal.emit(RegisterStatus.window_closed)
        elif self.registered:
            self.register_close_signal.emit(RegisterStatus.user_created)
        