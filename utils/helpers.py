import math
import sys
import os
import re
from typing import Pattern
from functools import reduce
import json
from random import randint

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QFont

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE'], 'Desktop'))

from widgetStyles.styles import placeholders
from widgetStyles.QCheckBox import WhiteEyeCheckBox, BlackEyeCheckBox
from database.model import Model
from utils.globals import WORDS, DB_PATH, FONT_NAME

layouts = [QGridLayout, QVBoxLayout, QHBoxLayout]

# clears the window so it can be repainted
def clear_window(container):
    # This is to remove the previous widgets that were painted so the widgets don't get added twice
    prev_items = container.count()

    # check if there are widgets
    if prev_items > 0:
        for i in range(container.count()):
            item = container.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                item.layout().deleteLater()
            elif item.spacerItem():
                container.removeItem(item.spacerItem())

class StyleSheet():
    def __init__(self, stylesheet):
        self.stylesheet = stylesheet
        settings = Model().read("settings")[0]
        # Get the nightmode setting
        self.settings_mode = "#000000" if int(settings[1]) else "#ffffff"
        # Set the contrast to the opposite of the nightmode
        self.settings_contrast = "#ffffff" if int(settings[1]) else  "#000000"
        self.settings_color = settings[3]

    def rgb(self, color):
        color /= 255
        if color <= 0.03928:
            return color / 12.92
        else:
            return math.pow( (color + 0.055) / 1.055, 2.4)

    def luminance(self, hex):
        r = int(hex[1:3], 16)
        g = int(hex[3:5], 16)
        b = int(hex[5:7], 16)
        array = list(map(self.rgb, [r, g, b]))
        return round( (array[0] * 0.2126 + array[1] * 0.7152 + array[2] * 0.0722), 4 )


    def contrast(self, c1, c2):
        color1 = self.luminance(c1)
        color2 = self.luminance(c2)
        if color1 > color2:
            return round((color1 + 0.05) / (color2 + 0.05), 1)
        elif color2 > color1:
            return round((color2 + 0.05) / (color1 + 0.05), 1)
        else:
            return 1
    
    def create(self):
        black_contrast = self.contrast(self.settings_color, "#000000")
        white_contrast = self.contrast(self.settings_color, "#ffffff")

        settings_button = "#000000" if black_contrast > white_contrast else "#ffffff"
        settings_default = self.settings_contrast

        # map the settings to the same index as the placeholders array
        # default will always be the opposite of the nightmode color
        values = [self.settings_color, self.settings_mode, settings_default, settings_button]

        stylesheet = reduce(lambda a, b: a + b, self.stylesheet)
        for i in range(len(placeholders)):
            stylesheet = re.sub(placeholders[i], values[i], stylesheet)
        return stylesheet


# Turn JSON data into dict
def json_to_dict(json_data):
    return json.loads(json_data)

def random_words(num_words=12, words=[]):
    word = WORDS[randint(0, 998)]
    
    if len(words) >= num_words: return words
    if word not in words: words.append(word)
             
    return random_words(num_words, words)

def get_checkbox():
    dark_mode_on = int(Model().read('settings')[0][1])
    checkbox = WhiteEyeCheckBox if dark_mode_on else BlackEyeCheckBox
    return checkbox

def set_font(font_list):
    for item in font_list:
        item.setFont(QFont(FONT_NAME))
        
def char_in_string(string: str, regex: Pattern) -> bool:
    result = re.findall(regex, string)
    return len(result) > 0

class LoginEvent:
    success = 14380754
    failed = 24985763
    closed = 35834975
    event_type = int    