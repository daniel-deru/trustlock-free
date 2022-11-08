from operator import itemgetter
import os
import sys
import pyperclip

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QFont


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.note_view import Ui_NoteView

from widgetStyles.Label import Label, LabelLarge
from widgetStyles.Dialog import Dialog
from widgetStyles.PushButton import PushButton100Width

from utils.helpers import StyleSheet, set_font

from database.model import Model


class NoteView(Ui_NoteView, QDialog):
    delete_signal = pyqtSignal(int)
    
    def __init__(self, note) -> None:
        super(NoteView, self).__init__()
        self.setupUi(self)
        self.read_styles()
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.note = note
        
        self.fill_data()

        self.btn_copy.clicked.connect(self.copy)
        self.btn_delete.clicked.connect(self.delete)
        
    def copy(self):
        pyperclip.copy(self.note[2])
        
    
    def delete(self):
        self.delete_signal.emit(self.note[0])
        self.close()
        
    def read_styles(self):
        widget_list = [
            Label, 
            Dialog, 
            PushButton100Width,
            LabelLarge("#lbl_name")
        ]
        stylesheet = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)

        font_list = [
            self.btn_copy,
            self.btn_delete,
            self.lbl_body,
            self.lbl_group,
            self.lbl_name
        ]
        set_font(font_list)
        
    def fill_data(self):
        self.lbl_name.setText(self.note[1])
        self.lbl_body.setText(self.note[2])
        
        groups = Model().read('groups')
        
        groups = sorted(groups, key=itemgetter(1))
        
        group = list(filter(lambda group: group[0] == int(self.note[3]), groups))
        self.lbl_group.setText(group[0][1])
        
    