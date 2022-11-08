import sys
import os
import re

from pyparsing import line
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import math

from PyQt5.QtWidgets import QDialog, QHBoxLayout, QWidget, QLabel, QGridLayout, QLineEdit, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon, QFont

from designs.python.crypto_words import Ui_CryptoWords

from utils.message import Message
from utils.globals import FONT_NAME
from utils.helpers import set_font, StyleSheet

from widgetStyles.Dialog import Dialog
from widgetStyles.PushButton import PushButton
from widgetStyles.Label import Label
from widgetStyles.LineEdit import LineEdit
from widgetStyles.Widget import Widget

class CryptoWords(Ui_CryptoWords, QDialog):
    filled_words: pyqtSignal = pyqtSignal(list)
    def __init__(self, num_words: int, words = None) -> None:
        super(CryptoWords, self).__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.set_style()
        
        self.num_words = num_words
        self.words = words
        
        self.displayWordBoxes()
        
        self.btn_save.clicked.connect(self.save)
        
    def set_style(self):
        styles = [
            PushButton,
            Dialog,
            Label,
            LineEdit
        ]
        
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        
        set_font([self.btn_save])
        
    def save(self):
        words_layout: QGridLayout = self.gbox_words
        words: list[str] = []
        
        valid_submit = True
        
        for i in range(words_layout.count()):
            widget_container: QWidget = words_layout.itemAt(i).widget()
            line_edit: QLineEdit = widget_container.layout().itemAt(1).widget()

            
            # line_edit: QLineEdit = password_widget.layout().itemAt(0).widget()

            if(type(line_edit) == QLineEdit):
                word: str = line_edit.text()
                if word: words.append(word)
                
        if(len(words) < self.num_words):
            Message(f"You have {len(words)} words but, you need {self.num_words} words. Please check for missing fields", "Missing Words").exec_()
            valid_submit = False
            
        word_string = "".join(words)
        valid_words = re.match(r"^[a-z]*$", word_string)

        if(not valid_words):
            Message("One or more words are not valid. Only alphabetic characters are allowed as valid words", "Invalid Word").exec_()
            valid_submit = False
            
        if(valid_submit):
            self.filled_words.emit(words)
            self.close()
        
    def displayWordBoxes(self):        
        COLUMNS: int = 3
        count: int = 1
        
        for i in range(math.ceil(self.num_words/COLUMNS)):
            for j in range(COLUMNS):
                hbox: QHBoxLayout = QHBoxLayout()
                hbox.setContentsMargins(0, 0, 0, 0)
                
                widget: QWidget = QWidget()
                widget.setContentsMargins(0, 0, 0, 0)

                self.number: QLabel = QLabel(f"{str(count).zfill(2)}. ")
                self.number.setFont(QFont(FONT_NAME))
                self.number.setMaximumWidth(40)
                
                lne_word: QLineEdit = QLineEdit()
                lne_word.setMinimumWidth(200)
                sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                lne_word.setSizePolicy(sizePolicy)

                word_index = count - 1
                # check if index for word is valid since the could only be 12 items but the loop can go to 21
                valid_word = self.words and word_index < len(self.words) 
                
                param = self.words[word_index] if valid_word else ""
                
                lne_word.setText(param)
                lne_word.textChanged.connect(self.fill_fields)
                set_font([lne_word])

                hbox.addWidget(self.number)
                hbox.addWidget(lne_word)

                widget.setLayout(hbox)

                if(count > self.num_words):
                    break
                self.gbox_words.addWidget(widget, i, j)
                
                count += 1
    @pyqtSlot(str)
    def fill_fields(self, text: str):
        words_list: list[str] = text.split(" ")
        num_words_array = [12, 15, 18, 21, 24]
        
        # Only loop and add words if the correct number of words have been specified
        if len(words_list) not in num_words_array: return
        
        for i in range(self.gbox_words.count()):
            widget_container: QWidget = self.gbox_words.itemAt(i).widget()
            line_edit: QLineEdit = widget_container.layout().itemAt(1).widget()
            
            word = words_list[i] if i < len(words_list) else ""
            
            # Prevent signal from firing when adding the data
            line_edit.blockSignals(True)
            
            line_edit.setText(word)
            # Re-enable signals after data is added
            line_edit.blockSignals(False)