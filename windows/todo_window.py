from operator import itemgetter
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from datetime import date, datetime, timedelta
from threading import Thread

from PyQt5.QtWidgets import QDialog, QWidget, QListView
from PyQt5.QtGui import QFont, QCursor, QIcon
from PyQt5.QtCore import QDate, Qt, pyqtSignal


from designs.python.todo_edit_window import Ui_todo_edit

from widgetStyles.PushButton import PushButton, IconToolButton
from widgetStyles.Label import Label
from widgetStyles.Calendar import Calendar
from widgetStyles.DateEdit import DateEditForm
from widgetStyles.ComboBox import ComboBox
from widgetStyles.LineEdit import LineEdit
from widgetStyles.Dialog import Dialog
from widgetStyles.TextEdit import TextEdit

from windows.group_window import GroupWindow

from database.model import Model
from utils.helpers import StyleSheet, set_font
from utils.globals import FONT_NAME

class TodoWindow(Ui_todo_edit, QDialog):
    todo_edit_signal = pyqtSignal(str)
    def __init__(self, todo=None):
        super(TodoWindow, self).__init__()
        self.todo: object or None = todo
        self.setupUi(self)
        self.set_groups()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.cmb_group.setView(QListView())
        self.cmb_group.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.read_styles()
        
        self.dtedt_date.setDate(date.today())
        if self.todo: self.set_data()

        self.btn_save.clicked.connect(self.save_clicked)
        self.tbtn_add_group.clicked.connect(self.add_new_group)
        
        self.integrate_google_calendar = Model().read("settings")[0][6]
        
    def add_new_group(self):
        group_window = GroupWindow()
        group_window.group_add_signal.connect(lambda: self.set_groups())
        group_window.exec_()
        
    def set_groups(self):
        groups = Model().read("groups")
        
        groups = sorted(groups, key=itemgetter(1))
        
        self.cmb_group.clear()
        
        for i in range(len(groups)):
            self.cmb_group.addItem(groups[i][1], groups[i][0])
            if self.todo and int(self.todo[5]) == groups[i][0]:
                self.cmb_group.setCurrentIndex(i)
        
        for i in range(len(groups)):
            if groups[i][1] == "Ungrouped":
                self.cmb_group.setCurrentIndex(i)

    def read_styles(self):
        widget_list = [
            Dialog,
            PushButton,
            LineEdit,
            Label,
            ComboBox,
            DateEditForm,
            Calendar,
            TextEdit,
            IconToolButton()
        ]

        stylesheet: str = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)

        font_widgets = [
            self.lbl_name,
            self.lbl_date,
            self.lbl_status,
            self.btn_save,
            self.cmbx_status,
            self.dtedt_date,
            self.lnedt_name,
            self.lbl_description,
            self.txe_description,
            self.lbl_group,
            self.cmb_group,
            self.cmb_group.view(),
            self.tbtn_add_group
        ]
        
        set_font(font_widgets)        

    
    def set_data(self):
        self.btn_save.setText("Update")
        if self.todo:
            self.lnedt_name.setText(self.todo[1])
            self.txe_description.setPlainText(self.todo[4])
            
            deadline_datetime = datetime.strptime(self.todo[3], "%Y-%m-%d")
            deadline = date(deadline_datetime.year, deadline_datetime.month, deadline_datetime.day)
            self.dtedt_date.setDate(deadline)
            
            self.cmbx_status.setCurrentIndex(int(self.todo[2]))
            

    def save_clicked(self):
        

        name: str = self.lnedt_name.text()
        description: str = self.txe_description.toPlainText()
        deadline: date = self.dtedt_date.date().toPyDate()
        group = self.cmb_group.currentData()
        deadline_text: str = datetime.strftime(deadline, "%Y-%m-%d")
        
        status_text = self.cmbx_status.currentText()
        status = "1" if status_text == "Complete" else "0"
        
            
        data = {
            'name': name, 
            'complete': status, 
            'deadline': deadline_text,
            'description': description,
            'group_id': group
        }

        if self.todo:
            Model().update('todos', data, self.todo[0])
        else:
            Model().save("todos", data)
        self.todo_edit_signal.emit("updated todo")
        self.close()
        

    def get_date(self):
        date = self.dtedt_date.date().toPyDate()
        self.todo['date'] = date
    
    def get_status(self):
        status: int = self.cmbx_status.currentIndex()
        self.todo['status'] = status
        