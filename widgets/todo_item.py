from datetime import date, datetime
import sys
import os

from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QToolButton
from PyQt5.QtCore import pyqtSignal, QSize, Qt
from PyQt5.QtGui import QIcon, QFont, QCursor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from database.model import Model

from widgetStyles.Frame import TodoFrame
from widgetStyles.Label import LabelMono
from widgetStyles.ToolButton import ToolButton
from widgetStyles.styles import StatusColor

from utils.helpers import StyleSheet, set_font

from windows.todo_window import TodoWindow
from windows.todo_view import TodoView

from database.model import Model

class TodoItem(QFrame):
    todo_item_signal = pyqtSignal(str)
    def __init__(self, todo):
        super(TodoItem, self).__init__()
        self.todo_id = todo[0]
        self.todo = todo[1]
        self.completed = int(todo[2])
        self.date = todo[3]
        self.todo_item = todo
        self.setupUI()
        self.read_styles()

        self.editButton.clicked.connect(self.editButtonClick)
        self.statusButton.clicked.connect(self.view_todo)

    
    def create_widget(self):
        return self        

    
    def setupUI(self):
        self.setObjectName("TodoItem")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        self.hbox = QHBoxLayout()
        self.hbox.setObjectName("hbox_todo_item")

        self.name = QLabel(self.todo)
        self.name.setObjectName("lbl_todo_name")
        self.name.setStyleSheet("color: #ffffff")

        self.lbl_date = QLabel(self.date)
        self.lbl_date.setObjectName("lbl_date")
        self.lbl_date.setStyleSheet("color: #ffffff")

        self.HSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        editIcon = QIcon(":/other/edit.png")
        self.editButton = QToolButton()
        self.editButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.editButton.setObjectName("btn_edit")
        self.editButton.setIcon(editIcon)
        self.editButton.setIconSize(QSize(20, 20))
        self.editButton.setCursor(QCursor(Qt.PointingHandCursor))

        icon = QIcon(":/input/eye_white_open.svg")
        self.statusButton = QToolButton()

        self.statusButton.setObjectName("btn_status")
        self.statusButton.setIcon(icon)
        self.statusButton.setIconSize(QSize(20, 20))
        self.statusButton.setCursor(QCursor(Qt.PointingHandCursor))



        self.hbox.addWidget(self.name)
        self.hbox.addWidget(self.lbl_date)
        self.hbox.addWidget(self.statusButton)
        self.hbox.addWidget(self.editButton)

        self.setLayout(self.hbox)


    def read_styles(self):
        datetime_deadline = datetime.strptime(self.date, "%Y-%m-%d")
        date_deadline = date(datetime_deadline.year, datetime_deadline.month, datetime_deadline.day)
        
        color = StatusColor.complete
        if not self.completed and date.today() > date_deadline:
            color = StatusColor.overdue
        elif not self.completed and not date.today() > date_deadline:
            color = StatusColor.incomplete
            
        styles = [
            LabelMono,
            TodoFrame(color),
            ToolButton
        ]
        
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)

        widget_list = [
           self.name,
           self.lbl_date
        ]

        set_font(widget_list)
    
    def view_todo(self):
        view_todo_window = TodoView(self.todo_item)
        view_todo_window.delete_signal.connect(self.delete_todo)
        view_todo_window.complete_signal.connect(self.complete_todo)
        view_todo_window.exec_()
    
    def delete_todo(self, id):
        Model().delete("todos", id)
        self.update()
    
    def complete_todo(self, id):
        Model().update("todos", {"complete": "1"}, id)
        self.update()

    # Fire an event when the edit button is clicked
    def editButtonClick(self):        
        todoEditWindow = TodoWindow(self.todo_item)
        todoEditWindow.todo_edit_signal.connect(self.update)
        todoEditWindow.exec_()

    # send signal to the main tab to update the view
    def update(self):
        self.todo_item_signal.emit(self.todo)


