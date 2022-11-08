import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, button, green, dark_blue, light_blue, default, orange, light_grey


ProgressBar = f"""
    QProgressBar {{
        color: {default};
        font-size: 16px;
        border-radius: 7px;
        background: transparent;
        height: 8px;
        width: 10px;
        text-align: right;
        margin-right: 60px;
    }}

    QProgressBar::chunk {{
        border-radius: 7px;
        background: {color};
    }}
    """
    
UpdateProgressBar = f"""
    QProgressBar {{
        color: {default};
        font-size: 16px;
        border-radius: 10px;
        background: {light_grey};
        height: 10px;
        width: 10px;
        text-align: right;
        margin-right: 40px;
    }}

    QProgressBar::chunk {{
        border-radius: 10px;
        background: {light_blue};
    }}
"""

def change_bar_color(color):
    ProgressBar = f"""
    QProgressBar {{
        color: {default};
        font-size: 16px;
        border-radius: 7px;
        background: transparent;
        height: 8px;
        width: 10px;
        text-align: right;
        margin-right: 60px;
    }}

    QProgressBar::chunk {{
        border-radius: 7px;
        background: {color};
    }}
    """
    return ProgressBar

custom_color_bar = change_bar_color

