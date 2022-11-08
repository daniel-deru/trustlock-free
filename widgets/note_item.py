import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QFrame, QSpacerItem, QSizePolicy, QToolButton
from PyQt5.QtCore import pyqtSignal, QSize, Qt, pyqtSlot
from PyQt5.QtGui import QIcon, QFont, QCursor


from windows.notes_window import Note_window
from windows.note_view import NoteView

from database.model import Model
from widgetStyles.Frame import Frame
from widgetStyles.Label import Label
from widgetStyles.ToolButton import ToolButton
from utils.helpers import StyleSheet, set_font



class NoteItem(QFrame):
    note_item_signal = pyqtSignal(int)
    def __init__(self, note):
        super(NoteItem, self).__init__()
        self.note = note
        self.id = note[0]
        self.note_name = note[1]
        self.body = note[2]
        self.setupUI()
        self.read_styles()

        self.btn_view.clicked.connect(self.view_note)
        self.btn_edit.clicked.connect(self.edit_note)


    def setupUI(self):
        dark_mode_on = int(Model().read("settings")[0][1])
        
        self.setObjectName("note_item")
        self.hbox = QHBoxLayout()
        self.hbox.setObjectName("hbox_note_item")

        self.name = QLabel(self.note_name)
        self.name.setObjectName("lbl_name")
        self.setStyleSheet("border: none;")

        self.HSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.btn_edit = QToolButton()
        self.btn_edit.setObjectName("btn_edit")
        edit_icon = "edit.png" if dark_mode_on else "edit_black"
        self.btn_edit.setIcon(QIcon(f":/other/{edit_icon}"))
        self.btn_edit.setIconSize(QSize(20, 20))
        self.btn_edit.setCursor(QCursor(Qt.PointingHandCursor))

        # This is the view button
        self.btn_view = QToolButton()
        self.btn_view.setObjectName("btn_delete")
        view_icon = "white" if dark_mode_on else "black"
        self.btn_view.setIcon(QIcon(f":/input/eye_{view_icon}_open.svg"))
        self.btn_view.setIconSize(QSize(20, 20))
        self.btn_view.setCursor(QCursor(Qt.PointingHandCursor))
        
        
        self.hbox.addWidget(self.name)
        self.hbox.addSpacerItem(self.HSpacer)
        self.hbox.addWidget(self.btn_view)
        self.hbox.addWidget(self.btn_edit)

        self.setLayout(self.hbox)


    def create(self):
        return self
    
    def view_note(self):
        view_note_window = NoteView(self.note)
        view_note_window.delete_signal.connect(self.delete_note)
        view_note_window.exec_()
    
    @pyqtSlot(int)
    def delete_note(self, id):
        Model().delete("notes", id)
        self.note_item_signal.emit(id)

    def edit_note(self):
        edit_window = Note_window(self.note)
        edit_window.note_window_signal.connect(lambda: self.note_item_signal.emit(self.id))
        edit_window.exec_()

    def read_styles(self):
        styles = [
            Frame,
            Label,
            ToolButton
        ]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        set_font([self.name])
        
        
