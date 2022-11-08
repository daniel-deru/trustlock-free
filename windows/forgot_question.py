import sys
import os
import math
import webbrowser

from PyQt5.QtWidgets import QDialog, QWidget, QLabel, QLineEdit, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.forgot_question import Ui_AnswerQuestionDialog

from utils.helpers import StyleSheet, set_font
from utils.message import Message

from widgetStyles.Dialog import Dialog
from widgetStyles.PushButton import PushButton, PushButtonLink
from widgetStyles.LineEdit import LineEdit
from widgetStyles.Label import Label

from database.model import Model

from windows.reset_password import ResetPassword


class PasswordQuestion(Ui_AnswerQuestionDialog, QDialog):
    passphrase_signal: pyqtSignal = pyqtSignal(bool)
    def __init__(self):
        super(PasswordQuestion, self).__init__()
        self.setupUi(self)
        self.read_styles()
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        
        self.create_fields() # create the line edit fields for the words

        user: list[tuple] = Model().read('user')[0]
        self.correct_phrase: str = user[4]
        
        self.btn_help.setStyleSheet(PushButtonLink())
        self.btn_help.clicked.connect(lambda: webbrowser.open_new_tab("https://lutiekhosting.com/"))

        self.btn_enter.clicked.connect(self.verify_answer)

    def read_styles(self):
        widgetlist: list[str] = [
            Dialog,
            PushButton,
            LineEdit,
            Label,
            PushButtonLink("#btn_help")
        ]

        stylesheet: str = StyleSheet(widgetlist).create()
        self.setStyleSheet(stylesheet)
        
        # self.btn_help.setStyleSheet(PushButtonLink)
        
        font_widgets = [
            self.lbl_question,
            self.btn_enter
        ]
            
        set_font(font_widgets)

    def verify_answer(self):
        empty_field: bool = False
        invalid_word: bool = False
        
        passphrase: list[str] = self.correct_phrase.split(" ")
        
        for i in range(self.gbox_words.count()):
            container: QHBoxLayout = self.gbox_words.itemAt(i).layout()
            field: QLineEdit = container.itemAt(1).widget()
            if not field.text():
                empty_field = True
                break
            elif field.text().strip() != passphrase[i]:
                invalid_word = True

        if(empty_field):
           return Message("Please fill in all the fields.", "Not Enough Words").exec_()
        elif(invalid_word):
           return Message("The passphrase is not correct.", "Incorrect Passphrase").exec_()

        self.close()
        reset_password_window = ResetPassword()
        reset_password_window.reset_signal.connect(lambda s: self.passphrase_signal.emit(s))
        reset_password_window.exec_()
        
    def create_fields(self):
        num_words: int = 12 # number of words in the passphrase
        cols: int = 3 # number of columns in the grid
        count: int = 1 # number to display next to the line edit
        
        # Loop to add the fields in the grid
        for i in range(math.ceil(num_words/cols)):
            for j in range(cols):
                container: QHBoxLayout = QHBoxLayout()
                number: str = f"{str(count).zfill(2)}. "
                count += 1
                label: QLabel = QLabel(number)
                line_edit: QLineEdit = QLineEdit()
                line_edit.textChanged.connect(self.fill_fields)
                
                set_font([line_edit, label]) # set the font for the widgets being added to the grid
                
                container.addWidget(label)
                container.addWidget(line_edit)
                self.gbox_words.addLayout(container, i, j)
    
    def fill_fields(self, text: str):
        words_list: list[str] = text.split(" ")
        if(len(words_list) != 12):
            return
        
        for i in range(self.gbox_words.count()):
            container: QHBoxLayout = self.gbox_words.itemAt(i).layout()
            field: QLineEdit = container.itemAt(1).widget()
            field.setText(words_list[i])