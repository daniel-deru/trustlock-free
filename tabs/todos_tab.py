from operator import itemgetter
import sys
import os
import math

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from database.model import Model
from designs.python.todo_widget import Ui_todo_tab

from widgets.todo_item import TodoItem
from widgets.filter_group_widget import FilterGroupWidget

from utils.helpers import StyleSheet, set_font
from utils.helpers import clear_window

from widgetStyles.PushButton import PushButton
from widgetStyles.LineEdit import LineEdit
from widgetStyles.Label import Label
from widgetStyles.DateEdit import DateEdit
from widgetStyles.Calendar import Calendar
from widgetStyles.ComboBox import ComboBox
from widgetStyles.ScrollBar import ScrollBar

from windows.todo_window import TodoWindow

class Todo_tab(Ui_todo_tab, QWidget):
    todo_signal = pyqtSignal(str)
    def __init__(self):
        super(Todo_tab, self).__init__()
        self.setupUi(self)
        self.filter_widget = FilterGroupWidget()
        self.filter_widget.group_changed_signal.connect(lambda group: self.display_todos(group))
        self.hbox_filter_widget.addWidget(self.filter_widget)
        self.read_style()
        
        initial_group = self.filter_widget.get_current_group()
        self.display_todos(initial_group)

        self.btn_add_todo.clicked.connect(self.add_todo)

        self.todo_signal.connect(self.update)
    
    def create_tab(self):
        return self

    def read_style(self):
        styles = [
            PushButton,
            LineEdit,
            Label,
            DateEdit,
            Calendar,
            # ComboBox,
            ScrollBar
        ]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        
        font_list = [
            self.btn_add_todo,
            self.lbl_todos
        ]
        set_font(font_list)

    def add_todo(self):
        todo_window = TodoWindow()
        todo_window.todo_edit_signal.connect(self.update)
        todo_window.exec_()


    def display_todos(self, group):
        clear_window(self.todo_container)
        todos = Model().read("todos")
        
        todos = sorted(todos, key=itemgetter(1))
        
        current_group = list(filter(lambda todo: todo[5] == str(group), todos))
        for i in range(len(current_group)):
            self.todo_item = TodoItem(current_group[i]).create_widget()
            self.todo_item.todo_item_signal.connect(self.update)
            
        COLUMNS = 2
        grid_items = []
        for i in range(math.ceil(len(current_group)/COLUMNS)):
            subarr = []
            for j in range(COLUMNS):
                if current_group:
                    subarr.append(current_group.pop(0))
            grid_items.append(subarr)
            
        for i in range(len(grid_items)):
            row = i
            for j in range(len(grid_items[i])):
                col = j
                self.todo_item = TodoItem(grid_items[i][j]).create_widget()
                self.todo_item.todo_item_signal.connect(self.update)
                self.todo_container.addWidget(self.todo_item, row, col)
    
    def update(self):
        clear_window(self.todo_container)
        initial_group = self.filter_widget.get_current_group()
        self.display_todos(initial_group)
        self.read_style()

        