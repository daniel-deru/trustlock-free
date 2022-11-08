import os
import sys
import pyperclip
import pyotp

from PyQt5.QtWidgets import (
    QDialog, 
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QMessageBox   
)
from PyQt5.QtGui import QIcon, QFont, QCloseEvent
from PyQt5.QtCore import QSize, QThread, Qt, pyqtSlot, pyqtSignal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.app_vault_view_window import Ui_AppVaultViewDialog

from utils.helpers import StyleSheet, json_to_dict, clear_window
from utils.message import Message

from widgetStyles.Label import Label
from widgetStyles.PushButton import PushButton
from widgetStyles.RadioButton import RadioButton
from widgetStyles.QCheckBox import WhiteEyeCheckBox, BlackEyeCheckBox
from widgetStyles.Dialog import Dialog
from widgetStyles.ToolButton import ToolButton

from windows.app_vault_window import AppVaultWindow

from database.model import Model

from workers.auto_type_worker import AutoType

from threads.totp_counter import totp_counter


class AppVaultView(Ui_AppVaultViewDialog, QDialog):
    previous_left = 0
    auto_type_thread_active = False
    update_signal = pyqtSignal(bool)
    
    def __init__(self, app):
        super(AppVaultView, self).__init__()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.app = app
        
        self.setupUi(self)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        
        self.set_icons()
        self.hideText()
        self.read_styles()
        
        self.should_update = False
        
        self.lbl_name_view.setText(self.app[2])
        
        self.data = json_to_dict(self.app[3])
        
        self.set_twofa_code()
        
        # The widgets in the vertical layout are [0,2,4,6,8] because of the hlines
        self.chk_username.stateChanged.connect(lambda checked: self.show_hidden("username", checked, 0))
        self.chk_email.stateChanged.connect(lambda checked: self.show_hidden("email", checked, 1))
        self.chk_password.stateChanged.connect(lambda checked: self.show_hidden("password", checked, 2))
        self.chk_password_exp.stateChanged.connect(lambda checked: self.show_hidden("password_exp", checked, 3))
        self.chk_path.stateChanged.connect(lambda checked: self.show_hidden("path", checked, 4))
        
        self.tbtn_username.clicked.connect(lambda: self.copy_data("username"))
        self.tbtn_email.clicked.connect(lambda: self.copy_data("email"))
        self.tbtn_password.clicked.connect(lambda: self.copy_data("password"))
        self.tbtn_password_exp.clicked.connect(lambda: self.copy_data("password_exp"))
        self.tbtn_twofa.clicked.connect(lambda: self.copy_twofa_code())
        self.tbtn_path.clicked.connect(lambda: self.copy_data("path"))
        
        self.btn_open.clicked.connect(self.open_app)
        self.btn_delete.clicked.connect(self.delete_secret)
        self.btn_edit.clicked.connect(self.edit_secret)
        
    @pyqtSlot()
    def delete_secret(self):
        confirm_delete = Message("Are you sure you want to delete this data", "Are You Sure?").prompt()
        
        if confirm_delete == QMessageBox.No: return
        
        Model().delete("vault", self.app[0])
        self.should_update = True
        self.close()
        
    @pyqtSlot()
    def edit_secret(self):
        edit_window = AppVaultWindow(self.app)
        edit_window.app_update_signal.connect(self.update_after_edit)
        edit_window.exec_()
        
    @pyqtSlot()
    def update_after_edit(self):
        # Get the new secrets
        secrets: list[list] = Model().read("vault")
        # Filter to get the correct one
        secret_filter = filter(lambda secret: secret[0] == self.app[0], secrets)
        # get list object from filter object
        secret = list(secret_filter)[0]
        
        self.app = secret
        self.data = json_to_dict(secret[3])
        
        self.lbl_name_view.setText(self.app[2])
        
        self.should_update = True       

    def set_twofa_code(self):
        try:
            self.data['twofa_code']
        except:
            self.delete_twofa_code()
            return
        
        if(self.data['twofa_code']):
            totp_counter(self, self.data['twofa_code'])
            self.chk_twofa.stateChanged.connect(self.get_twofa_code)
            self.tbtn_twofa.clicked.connect(self.copy_twofa_code)
        else:
            self.delete_twofa_code()
    
    def delete_twofa_code(self):
        # get the twofa container
        index: int = self.vbox_data.count() - 1
        container_layout: QVBoxLayout = self.vbox_data.itemAt(index).layout()
        
        # Remove the line
        line = container_layout.itemAt(1).widget()
        line.setParent(None)
        
        # Get the container with the data
        data_container: QHBoxLayout = container_layout.itemAt(0).layout()

        # Get the widgets
        label = data_container.itemAt(0).widget()
        label2 = data_container.itemAt(1).widget()
        countdown = data_container.itemAt(3).widget()
        toolbutton = data_container.itemAt(4).widget()
        checkbox = data_container.itemAt(5).widget()
        
        # Remove the widgets
        label.setParent(None)
        label2.setParent(None)
        countdown.setParent(None)
        toolbutton.setParent(None)
        checkbox.setParent(None)
            
        
    @pyqtSlot()
    def copy_twofa_code(self):
        totp = pyotp.TOTP(self.data['twofa_code'])
        current = totp.now()
        pyperclip.copy(current)
        
    @pyqtSlot(int)
    def get_twofa_code(self, event):
        dots = u"\u2022"*10
        if event:
            totp = pyotp.TOTP(self.data['twofa_code'])
            current = totp.now()
            self.lbl_twofa.setText(current)
        else:
            self.lbl_twofa.setText(dots)
        
    
    def read_styles(self):
        settings = Model().read('settings')[0]
        dark_mode_on = int(settings[1])
        checkbox = WhiteEyeCheckBox if dark_mode_on else BlackEyeCheckBox
        
        widget_list = [checkbox, Label, PushButton, RadioButton, Dialog, ToolButton]
        stylesheet = StyleSheet(widget_list).create()
        
        self.setStyleSheet(stylesheet)
        
        font_name = settings[2]
        
        font_widgets = [
            self.lbl_email,
            self.lbl_password,
            self.lbl_path,
            self.lbl_username,
            self.lbl_email_view,
            self.lbl_name_view,
            self.lbl_password_view,
            self.lbl_path_view,
            self.lbl_username_view,
            self.btn_open,
            self.lbl_password_exp,
            self.lbl_password_exp_view,
            self.lbl_twofa,
            self.lbl_twofa_view,
            self.lbl_counter,
            self.btn_edit,
            self.btn_delete  
        ]
        
        widget: QWidget
        
        for widget in font_widgets:
            widget.setFont(QFont(font_name))
        
        
    def hideText(self):
        dots = u"\u2022"*10
        for i in range(self.vbox_data.count()):
            vertical_layout = self.vbox_data.itemAt(i).layout()
            data_label = vertical_layout.itemAt(0).layout().itemAt(1).widget()
            data_label.setText(dots)
        
    def show_hidden(self, field_name: str, checked: int, label_index: int):
        vertical_container = self.vbox_data.layout().itemAt(label_index).layout()
        label = vertical_container.itemAt(0).layout().itemAt(1).widget()
        
        dots = u"\u2022"*10
        if checked:
            label.setText(self.data[field_name])
        else:
            label.setText(dots)
            
    def copy_data(self, field_name: str):
        pyperclip.copy(self.data[field_name])
        
    def set_icons(self):
        dark_mode_on = Model().read('settings')[0][1]
        icon_color = "white" if int(dark_mode_on) else "black"
        icon = QIcon(f":/input/copy_{icon_color}")  
         
        buttons = [
            self.tbtn_email,
            self.tbtn_password,
            self.tbtn_password_exp,
            self.tbtn_path,
            self.tbtn_twofa,
            self.tbtn_username
        ]
    
        for button in buttons:
            button.setIcon(icon)
            button.setIconSize(QSize(25, 25))
        
    def open_app(self):
        os.startfile(self.data['path'])
        if not self.auto_type_thread_active:
            self.activate_auto_type()
             
    def activate_auto_type(self):
        things_to_type = [self.data['email'], self.data['password']]
        
        self.auto_type_thread = QThread()
        self.auto_typer = AutoType(things_to_type)
        
        self.auto_typer.moveToThread(self.auto_type_thread)
        
        # self.auto_typer.finished.connect(self.auto_type_thread_off)
        
        self.auto_type_thread.started.connect(self.auto_typer.auto_type)
        
        self.auto_typer.finished.connect(self.auto_typer.deleteLater)
        self.auto_typer.finished.connect(self.auto_type_thread.exit)
        self.auto_typer.finished.connect(self.auto_type_thread.quit)
        self.auto_type_thread.finished.connect(self.auto_type_off)
        
        self.auto_type_thread.start()
        self.auto_type_thread_active = True
        
    def auto_type_thread_off(self):
        self.auto_type_thread_active = False
        
    def auto_type_off(self):
        self.auto_type_thread.deleteLater
        self.auto_type_thread_active = False
        
    def closeEvent(self, event: QCloseEvent) -> None:
        if self.should_update:
            self.update_signal.emit(True)
            
        return super().closeEvent(event)