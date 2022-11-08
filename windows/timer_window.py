import os
import sys

from PyQt5.QtWidgets import QDialog, QLCDNumber
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.timer_window import Ui_Timer
from utils.helpers import StyleSheet, set_font
from database.model import Model

from widgetStyles.PushButton import PushButton
from widgetStyles.Label import Label
from widgetStyles.Dialog import Dialog
from widgetStyles.HSlider import HSlider
from widgetStyles.LCDNumber import LCDNumber

class Timer(Ui_Timer, QDialog):
    def __init__(self):
        super(Timer, self).__init__()
        self.setupUi(self)

        time = Model().read("settings")[0][5]
        self.lcd_timer.display(time)
        self.hslide_timer.setValue(int(time))

        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.read_styles()
        self.hslide_timer.valueChanged.connect(self.slider)
        self.btn_save.clicked.connect(self.save)
    
    def slider(self):
        self.lcd_timer.display(self.hslide_timer.value())

    def read_styles(self):
        styles = [
            Dialog,
            PushButton,
            Label,
            HSlider,
            LCDNumber
            ]
        self.lcd_timer.setSegmentStyle(QLCDNumber.Flat)
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        
        widget_list = [
            self.btn_save,
            self.lbl_vault_timer
        ]
        set_font(widget_list)
    
    def save(self):
        Model().update("settings", {"timer": self.hslide_timer.value()}, 'settings')
        self.close()