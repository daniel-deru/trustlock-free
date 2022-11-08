import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon

from designs.python.group_view_window import Ui_GroupWindow

from utils.helpers import StyleSheet

from widgetStyles.Label import Label, LabelLarge
from widgetStyles.PushButton import PushButton
from widgetStyles.Dialog import Dialog

from utils.helpers import set_font
from utils.message import Message

from database.model import Model

class GroupViewWindow(Ui_GroupWindow, QDialog):
    delete_group_signal = pyqtSignal(int)
    def __init__(self, group) -> None:
        super(GroupViewWindow, self).__init__()
        self.group = group
        self.has_data: bool = False
        self.setupUi(self)
        self.read_styles()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.display_data()
        
        
        self.btn_delete.clicked.connect(self.delete)
        
        if self.group['name'] == "Ungrouped":
            self.btn_delete.hide()
        
    @pyqtSlot()
    def delete(self):
        if self.has_data:
           return Message("Cannot delete group because there is still some data in te group", "Cannot Delete Group").exec_()
        # Send signal back to group widget with the id of the group to delete
        Model().delete("groups", self.group['id'])
        self.delete_group_signal.emit(self.group['id'])
        self.close()
        
    def read_styles(self):
        widget_list = [
            Dialog, 
            PushButton, 
            Label,
            LabelLarge("#lbl_group_name")
        ]
        
        stylesheet = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)
        
        font_list = [
            self.lbl_apps,
            self.lbl_apps_display,
            self.lbl_description,
            self.lbl_group_name,
            self.lbl_notes,
            self.lbl_notes_display,
            self.lbl_todos,
            self.lbl_todos_display,
            self.lbl_vault,
            self.lbl_vault_display,
            self.btn_delete
        ]
        set_font(font_list)
        
    def display_data(self):
        self.lbl_group_name.setText(self.group['name'])
        self.lbl_description.setText(self.group['description'])
        
        display_widget = {
            'apps': self.lbl_apps_display,
            'vault': self.lbl_vault_display,
            'notes': self.lbl_notes_display,
            'todos': self.lbl_todos_display
        }


        for key, value in display_widget.items():
            total = self.group['data'][key]
            if total > 0: self.has_data = True
            value.setText(str(total))     
    