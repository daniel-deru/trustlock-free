import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default, dark_blue, light_blue
import assets.resources

DateEdit = f"""
    QDateEdit {{
        border: none;
        color: {default};
        font-size: 12px;
        height: 30px;
    }}
    QDateEdit::drop-down {{
        background-color: {mode};
        border: 1px solid {light_blue};
        color: {default};
        padding: 5px;
        border-radius: 5px;
        width: 40px;
        image: url(:/other/calendar.svg);
    }}
"""

DateEditForm = f"""
    QDateEdit {{
        border: 1px solid {light_blue};
        color: {default};
        font-size: 16px;
        border-radius: 5px;
        height: 30px;
        background-color: {mode};
    }}
    QDateEdit::drop-down {{
        background-color: {mode};
        border: none;
        color: {default};
        padding: 5px;
        border-radius: 5px;
        width: 40px;
        image: url(:/other/calendar.svg);
    }}
"""