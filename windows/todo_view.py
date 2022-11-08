import os
import sys
from datetime import date, datetime

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QFont


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.todo_view_window import Ui_TodoViewWindow

from widgetStyles.Label import Label
from widgetStyles.Dialog import Dialog
from widgetStyles.PushButton import PushButton100Width

from utils.helpers import StyleSheet, set_font

from database.model import Model


class TodoView(Ui_TodoViewWindow, QDialog):
    delete_signal = pyqtSignal(int)
    complete_signal = pyqtSignal(int)
    
    def __init__(self, todo) -> None:
        super(TodoView, self).__init__()
        self.setupUi(self)
        self.read_styles()
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.todo = todo
        
        self.fill_data()
        
        self.btn_complete.clicked.connect(self.complete)
        self.btn_delete.clicked.connect(self.delete)
        
    def complete(self):
        self.complete_signal.emit(self.todo[0])
        self.close()
        
    
    def delete(self):
        self.delete_signal.emit(self.todo[0])
        self.close()
        
    def read_styles(self):
        widget_list = [Label, Dialog, PushButton100Width]
        stylesheet = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)

        font_list = [
            self.btn_complete,
            self.btn_delete,
            self.lbl_deadline,
            self.lbl_deadline_display,
            self.lbl_description,
            self.lbl_description_display,
            self.lbl_name,
            self.lbl_name_display,
            self.lbl_status,
            self.lbl_status_display
        ]
        
        set_font(font_list)
        
    def fill_data(self):
        self.lbl_name_display.setText(self.todo[1])
        
        completed = int(self.todo[2])

        self.lbl_status_display.setText("Complete")
        if not completed:
            self.lbl_status_display.setText("Incomplete")
            
            datetime_deadline: datetime = datetime.strptime(self.todo[3], "%Y-%m-%d")
            date_deadline: date = date(datetime_deadline.year, datetime_deadline.month, datetime_deadline.day)
            
            if date_deadline < date.today():
                self.lbl_status_display.setText("Overdue")
        
        self.lbl_deadline_display.setText(self.todo[3])
        self.lbl_description_display.setText(self.todo[4])
        
    