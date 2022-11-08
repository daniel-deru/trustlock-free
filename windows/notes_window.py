from operator import itemgetter
import os
import sys
import pyperclip

from PyQt5.QtWidgets import QDialog, QTextEdit, QListView
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon, QTextCursor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


from designs.python.note_window import Ui_Note_Window


from utils.message import Message
from utils.helpers import StyleSheet, set_font

from database.model import Model

from windows.group_window import GroupWindow

from widgetStyles.PushButton import PushButton, IconToolButton
from widgetStyles.LineEdit import LineEdit
from widgetStyles.QCheckBox import CheckBoxSquare
from widgetStyles.TextEdit import TextEdit
from widgetStyles.Dialog import Dialog
from widgetStyles.ComboBox import ComboBox
from widgetStyles.Label import Label


class Note_window(Ui_Note_Window, QDialog):
    note_window_signal = pyqtSignal(str)
    def __init__(self, edit_note=None):
        super(Note_window, self).__init__()
        self.note = edit_note

        self.setupUi(self)
        self.set_groups()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.cmb_groups.setView(QListView())
        self.cmb_groups.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)

        self.custom_text_edit = CustomTextEdit().create()
        self.vbox_body.addWidget(self.custom_text_edit)

        self.read_styles()
        self.set_note()

        self.chkbx_edit.stateChanged.connect(self.set_delete_active) 
        self.btn_save.clicked.connect(self.save_clicked)
        self.btn_copy_note.clicked.connect(self.copy_text)
        self.tbtn_add_group.clicked.connect(self.add_new_group)
        
    def add_new_group(self):
        group_window = GroupWindow()
        group_window.group_add_signal.connect(lambda: self.set_groups())
        group_window.exec_()
        
    def set_note(self):
        if not self.note: return
        
        self.lnedt_title.setText(self.note[1])
        self.custom_text_edit.setPlainText(self.note[2])
        self.btn_save.setText("Update")
        self.text = self.note[2]
        
    def set_groups(self):
        groups = Model().read('groups')
        
        groups = sorted(groups, key=itemgetter(1))
        
        self.cmb_groups.clear()
        
        for i in range(len(groups)):
            self.cmb_groups.addItem(groups[i][1], groups[i][0])
                
        for i in range(len(groups)):
            if groups[i][1] == "Ungrouped":
                self.cmb_groups.setCurrentIndex(i)
            if self.note and int(self.note[3]) == groups[i][0]:
                self.cmb_groups.setCurrentIndex(i)
    
    def set_delete_active(self):
            delete_checked = self.chkbx_edit.isChecked()
            if delete_checked:
                self.custom_text_edit.delete_signal.emit(True)
            elif not delete_checked:
                self.custom_text_edit.delete_signal.emit(False)


    def save_clicked(self):
        name = self.lnedt_title.text()
        body = self.custom_text_edit.toPlainText()
        group = self.cmb_groups.currentData()
        
        if not self.lnedt_title.text():
            message = Message("Please enter a title for your note.", "Note")
            message.exec_()
        else:
            make_note = {
                    'name': name,
                    'body': body,
                    'group_id': group
                }
            if not self.note:
                Model().save("notes", make_note)
            else:
                Model().update("notes", make_note, self.note[0])
            self.note_window_signal.emit("note saved")
            self.close()

    def copy_text(self):
        body = self.custom_text_edit.toPlainText()
        pyperclip.copy(body)
        pass

    def read_styles(self):
        styles = [
            PushButton,
            LineEdit,
            CheckBoxSquare,
            TextEdit,
            Dialog,
            ComboBox,
            Label,
            IconToolButton()
        ]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        
        font_list = [
            self.chkbx_edit,
            self.btn_save,
            self.custom_text_edit,
            self.btn_copy_note,
            self.lnedt_title,
            self.cmb_groups,
            self.cmb_groups.view(),
            self.lbl_group,
            self.lbl_name,
            self.lbl_body,
            self.tbtn_add_group
        ]
        set_font(font_list)



# Custom Text Edit class to get access to the keypress event in order to stop users from deleting content
class CustomTextEdit(QTextEdit):
    # This is a custom signal to check if the textedit is editable
    delete_signal = pyqtSignal(bool)
    def __init__(self):
        super(CustomTextEdit, self).__init__()

        self.delete_active = False

        self.delete_signal.connect(self.set_delete_status)
    
    def set_delete_status(self, signal):
        self.delete_active = signal

    def keyPressEvent(self, event):
        if not self.delete_active:
            if event.key() == Qt.Key_Delete:
                self.set_text(self.toPlainText())
                self.moveCursor(QTextCursor.End)
            elif event.key() == Qt.Key_Backspace:
                self.set_text(self.toPlainText())
        super().keyPressEvent(event)
        
    
    def create(self):
        return self

    def set_text(self, text):
        self.setPlainText(text)
