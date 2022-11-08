import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default, light_blue

TextEdit = f"""
    QTextEdit{{
        background-color: {mode};
        color: {default};
        border-radius: 5px;
        font-size: 16px;
        border: 1px solid {light_blue};
    }}
"""