from operator import itemgetter
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import math

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont



from database.model import Model
from designs.python.notes_widget import Ui_notes_tab
from windows.notes_window import Note_window

from widgets.note_item import NoteItem
from widgets.filter_group_widget import FilterGroupWidget

from utils.helpers import clear_window
from widgetStyles.PushButton import PushButton
from widgetStyles.QCheckBox import CheckBoxSquare
from widgetStyles.ComboBox import ComboBox
from widgetStyles.Label import Label
from widgetStyles.ScrollBar import ScrollBar
from utils.helpers import StyleSheet, set_font




class Notes_tab(Ui_notes_tab, QWidget):
    note_signal = pyqtSignal(str)
    def __init__(self):
        super(Notes_tab, self).__init__()
        self.setupUi(self)
        
        self.filter_widget = FilterGroupWidget()
        self.filter_widget.group_changed_signal.connect(lambda group: self.display_note(group))
        
        self.hbox_filter_widget.addWidget(self.filter_widget)
        self.read_styles()
        
        initial_group = self.filter_widget.get_current_group()
        self.display_note(initial_group)

        self.btn_note.clicked.connect(self.add_note)
        self.note_signal.connect(self.update_window)

    def create_tab(self):
        return self

    def read_styles(self):
        styles = [
            CheckBoxSquare, 
            PushButton, 
            # ComboBox, 
            Label,
            ScrollBar
        ]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        
        font_list = [
            self.btn_note,
            self.lbl_notes
        ]
        
        set_font(font_list)


    def add_note(self):
        note_window = Note_window()
        note_window.note_window_signal.connect(self.update_window)
        note_window.exec_()

    def display_note(self, group):
        clear_window(self.gbox_note_container)
        notes = Model().read("notes")
        
        notes = sorted(notes, key=itemgetter(1))
        
        current_group = list(filter(lambda note: note[3] == str(group), notes))
        grid_items = []
        for i in range(math.ceil(len(current_group)/2)):
            subarr = []
            for j in range(2):
                if current_group:
                    subarr.append(current_group.pop(0))
            grid_items.append(subarr)
            
        for i in range(len(grid_items)):
            row = i
            for j in range(len(grid_items[i])):
                col = j
                self.note = NoteItem(grid_items[i][j]).create()
                self.note.note_item_signal.connect(self.update_window)
                self.gbox_note_container.addWidget(self.note, row, col)
    
    def update_window(self):
        self.read_styles()
        initial_group = self.filter_widget.get_current_group()
        self.display_note(initial_group)
        # self.note.note_item_signal.emit("signal")
        





