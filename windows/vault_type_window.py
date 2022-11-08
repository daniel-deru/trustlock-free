import os
import sys

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.vault_type_window import Ui_VaultTypeDialog

from widgetStyles.Dialog import Dialog
from widgetStyles.PushButton import ButtonFullWidth, PushButton
from widgetStyles.styles import VAULT_BUTTON_COLORS
from widgetStyles.Frame import vault_type_frame
from widgetStyles.Label import Label

from utils.helpers import StyleSheet, set_font

class VaultType(Ui_VaultTypeDialog, QDialog):
    vault_type_signal = pyqtSignal(str)
    def __init__(self):
        super(Ui_VaultTypeDialog, self).__init__()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.setupUi(self)
        self.setMinimumWidth(100)
        self.readStyles()

        self.btn_general.clicked.connect(self.open_general_vault)
        self.btn_app.clicked.connect(self.open_app_vault)
        self.btn_crypto.clicked.connect(self.open_crypto_vault)

    def readStyles(self):
        widget_list = [
            PushButton, 
            Dialog,
            vault_type_frame("#frame_crypto_wallet", VAULT_BUTTON_COLORS['crypto']),
            vault_type_frame("#frame_app_vault", VAULT_BUTTON_COLORS['app']),
            vault_type_frame("#frame_general_vault", VAULT_BUTTON_COLORS['general']),
            Label
        ]

        stylesheet = StyleSheet(widget_list).create()

        self.setStyleSheet(stylesheet)
        
        font_widget = [
            self.btn_app,
            self.btn_crypto,
            self.btn_general,
            self.lbl_app_heading,
            self.lbl_crypto_heading,
            self.lbl_general_heading,
            self.lbl_app_desc,
            self.lbl_crypto_desc,
            self.lbl_general_desc
        ]
        
        set_font(font_widget)
        
        self.btn_app.setStyleSheet(f"background-color: {VAULT_BUTTON_COLORS['app']};border: 1px solid {VAULT_BUTTON_COLORS['app']};")
        self.btn_crypto.setStyleSheet(f"background-color: {VAULT_BUTTON_COLORS['crypto']};border: 1px solid {VAULT_BUTTON_COLORS['crypto']};")
        self.btn_general.setStyleSheet(f"background-color: {VAULT_BUTTON_COLORS['general']};border: 1px solid {VAULT_BUTTON_COLORS['general']};")
        
        self.btn_app.setIcon(QIcon(":/button_icons/app"))        
        self.btn_crypto.setIcon(QIcon(":/button_icons/crypto"))        
        self.btn_general.setIcon(QIcon(":/button_icons/general"))      
        
          
    def open_general_vault(self):
        self.vault_type_signal.emit("general")
        self.close()

    def open_app_vault(self):
        self.vault_type_signal.emit("app")
        self.close()

    def open_crypto_vault(self):
        self.vault_type_signal.emit("crypto")
        self.close()

