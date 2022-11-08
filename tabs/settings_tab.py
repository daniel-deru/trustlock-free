import sys
import os
import shutil
import json

from PyQt5.QtWidgets import QWidget, QFileDialog, QPushButton
from PyQt5.QtCore import pyqtSignal, Qt, QSize, pyqtSlot
from PyQt5.QtGui import QFont, QIcon, QPixmap, QCursor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.settings_tab import Ui_Settings_tab

from widgetStyles.Label import Label
from widgetStyles.PushButton import IconButton
from widgetStyles.QCheckBox import SettingsCheckBox
from widgetStyles.ComboBox import ComboBox
from widgetStyles.ScrollBar import ScrollBar
from widgetStyles.ToolButton import ToolButton
from widgetStyles.TabBar import RegisterTabBar

from utils.message import Message
from utils.helpers import LoginEvent, StyleSheet, set_font
from utils.globals import DB_PATH, PATH, DB_NAME, DESKTOP
from utils.enums import TwofaStatus

from database.model import Model


from windows.forgot_question import PasswordQuestion
from windows.reset_password import ResetPassword
from windows.twofa_window import TwofaDialog
from windows.generate_password import GeneratePasswordWindow
from windows.setup_window import InitialSetup
from windows.groups_window import GroupsWindow
from windows.timer_window import Timer
from windows.login_window import Login

class SettingsTab(Ui_Settings_tab, QWidget):
    settings_signal = pyqtSignal(str)
    settings_update_signal = pyqtSignal(str)
    logout_signal = pyqtSignal(bool)
    
    def __init__(self):
        super(SettingsTab, self).__init__()
        self.setupUi(self)
        self.read_styles()

        self.logged_in = False
        self.set_checkboxes()
        self.set_btn_icons()



        # checkbox signals        
        self.chkbox_nightmode.stateChanged.connect(self.set_night_mode)
        self.chkbox_2fa.stateChanged.connect(self.twofa)
        
        self.btn_forgot_password.clicked.connect(self.forgot_password_clicked)
        self.btn_save_local.clicked.connect(self.save_local)
        self.btn_restore_local.clicked.connect(self.restore_from_local)
        self.btn_generate_password.clicked.connect(self.generate_password)
        self.btn_setup.clicked.connect(self.setup_wizard)
        self.btn_groups.clicked.connect(self.manage_groups)
        self.btn_update_password.clicked.connect(self.updatePassword)
        
        self.btn_timer.clicked.connect(self.timer)
        self.btn_lock.clicked.connect(lambda: self.tab_widget_settings.setCurrentIndex(0))

        # connect the custom signals to the slots
        self.settings_signal.connect(lambda: self.updateWindow(False))
        self.settings_update_signal.connect(lambda: self.updateWindow(False))
        self.logout_signal.connect(lambda s: self.tab_widget_settings.setCurrentIndex(0) if s else None)
        
        self.tab_widget_settings.currentChanged.connect(self.tab_changed)

    
    @pyqtSlot()
    def tab_changed(self):
        current_index = self.tab_widget_settings.currentIndex()
        
        if current_index == 1 and not self.logged_in:
            self.tab_widget_settings.setCurrentIndex(0)
            login_window = Login()
            login_window.login_status.connect(self.login)
            login_window.exec_()
        else:
            self.logged_in = False
            
    @pyqtSlot(str)
    def login(self, signal: str):
        if signal == "success":
            self.logged_in = True
            self.tab_widget_settings.setCurrentIndex(1)
    
    @pyqtSlot()
    def timer(self):
        timer_window = Timer()
        timer_window.exec_()
        
    @pyqtSlot()
    def updatePassword(self):
        # Request login even if user is logged in
        # Pass in a variable to determin which signals to send
        login_window = Login(update_password=True)
        login_window.update_password_status.connect(self.update_password)
        login_window.exec_()

    
    @pyqtSlot(str)
    def update_password(self, status: str):
        if(status == "success"):
            update_password_window = ResetPassword(False)
            update_password_window.exec_()
        
    def set_checkboxes(self):
        settings = Model().read('settings')[0]
        # Set the default value of the settings
        self.chkbox_nightmode.setChecked(int(settings[1]))
        
        self.chkbox_2fa.blockSignals(True)
        self.chkbox_2fa.setChecked(int(settings[7]))
        self.chkbox_2fa.blockSignals(False)
        
    def manage_groups(self):
        GroupsWindow().exec_()
        
    def setup_wizard(self):
        setup_wizard = InitialSetup()
        setup_wizard.setup_finished.connect(self.updateWindow)
        setup_wizard.exec_()
        
    def generate_password(self):
        generate_password = GeneratePasswordWindow()
        generate_password.exec_()
    
    def create_tab(self):
        return self

    # color is at index 3 and nightmode is at index 1
    def set_night_mode(self, checked):
        if checked:
            Model().update("settings", {'nightmode': "1"}, 'settings')
        else:
            Model().update("settings", {'nightmode': "0"}, 'settings')
            
        self.updateWindow()
        
    
    # 2fa slot
    def twofa(self, checked):
        if checked:
            twofa_window = TwofaDialog()
            twofa_window.twofa_status.connect(self.twofa_status)
            twofa_window.exec_()
        else:
            Model().update('user', {'twofa_key': None}, 'user')
            Model().update("settings", {'twofa': '0'}, 'settings')
    
    @pyqtSlot(TwofaStatus)       
    def twofa_status(self, status: TwofaStatus):
        if status == TwofaStatus.failure:
            self.chkbox_2fa.setChecked(False)
            self.chkbox_2fa.setCheckState(Qt.Unchecked)
    
    def updateWindow(self, send_signal: bool = True):
        self.read_styles()
        self.set_checkboxes()
        if send_signal: self.settings_signal.emit("settings")

    def read_styles(self):
        styles = [
            Label, 
            SettingsCheckBox, 
            ComboBox, 
            ScrollBar, 
            IconButton,
            ToolButton, # this is for the google button
            RegisterTabBar
        ]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        
        self.tab_widget_settings.tabBar().setCursor(QCursor(Qt.PointingHandCursor))
        
        font_widgets = [
            self.lbl_2fa,
            self.lbl_night_mode,
            self.lbl_forgot_password,
            self.lbl_save_local,
            self.lbl_restore_local,
            self.lbl_generate_password,
            self.lbl_setup,
            self.lbl_groups,
            self.lbl_update_password,
            self.lbl_timer,
            self.tab_widget_settings,
            self.lbl_lock
        ]
        
        set_font(font_widgets)
            
    def set_btn_icons(self):
        
        self.btn_generate_password.setIcon(QIcon(":/button_icons/password"))
        self.btn_generate_password.setIconSize(QSize(30, 20))
        
        button_icon_list = [
            [self.btn_forgot_password, ":/button_icons/reset"],
            [self.btn_lock, ":/button_icons/lock"],
            [self.btn_restore_local, ":/button_icons/drive_download"],
            [self.btn_save_local, ":/button_icons/drive_upload"],
            [self.btn_setup, ":/button_icons/setup"],
            [self.btn_groups, ":/button_icons/group"],
            [self.btn_update_password, ":/button_icons/reset"],
            [self.btn_timer, ":/button_icons/timer"],
        ]
        
        for button, icon in button_icon_list:
            button: QPushButton
            button.setIcon(QIcon(icon))
            button.setIconSize(QSize(20, 20))
    

    def forgot_password_clicked(self):
        ask_question = PasswordQuestion()
        ask_question.passphrase_signal.connect(lambda: self.updateWindow())
        ask_question.exec_()

        
    def save_local(self):
        path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if path: shutil.copy(f"{DB_PATH}{DB_NAME}", f"{path}/{DB_NAME}")

        
    def restore_from_local(self):
        file = QFileDialog.getOpenFileName(self, "Choose a file", DESKTOP, f"DB File ({DB_NAME})")[0]
        
        if not file: 
            return

        valid_db, message = self.compare_dbs(file)

        if(not valid_db):
            return Message(message, "Sync Failed")

        shutil.copy(file, f"{DB_PATH}{DB_NAME}")
        self.updateWindow()
        Message("Local data sync was successful.", "Sync Successful").exec_()
            
    def compare_dbs(self, new_db_path):
        new_db = None
    
        try: 
            new_db = Model(new_db_path)
        except Exception:
            return [False, "Unable to open database"]
        
        new_db_user = new_db.read('user')
        
        if(len(new_db_user) < 1):
            return [False, "Invalid database"]
        
        new_db_passphrase = new_db_user[0][4]
        passphrase = Model().read('user')[0][4]
        
        if(new_db_passphrase != passphrase):
            return [False, "The account you are trying to restore is not the same as the account you currently have."]
        
        return [True, None]
    
    # check if the new db is valid and replace old db with new db
    def update_db(self, name: str or None):
        if(not name):
            self.loading.close()
            return Message("The database does not exist or there is a network error", "Sync Failed").exec_()
        
        valid_db, message = Model().valid_account(f"{DB_PATH}{name}")
        
        if(not valid_db):
            self.loading.close()
            return Message(message, "Sync Error").exec_()

        shutil.move(f"{DB_PATH}{name}", f"{DB_PATH}{DB_NAME}")
        Message("Sync was successful.", "Sync Successful").exec_()
        
        # Close the loading dialog after thread is finished
        self.loading.close()
        
