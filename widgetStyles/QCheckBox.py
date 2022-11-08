import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default
from database.model import Model

import assets.resources

dark_mode_on = int(Model().read('settings')[0][1])
SIZE = 25
RATIO = 2
width = SIZE * RATIO
height = SIZE * 1

SQUARE_SIZE = 30
SQUARE_RATIO = 4

square_width= SQUARE_SIZE * SQUARE_RATIO
square_height = SQUARE_SIZE

toggle = "toggle-off.svg"

CheckBox = f"""
    QCheckBox {{
        color: {default};
        font-size: 16px;
        border-radius: 5px;
    }}

    QCheckBox::indicator:checked {{
        image: url(:/input/toggle-on.svg);
        width: {width}px;
        height: {height}px;
        max-width: {width}px;
        max-height: {height}px;
    }}

    QCheckBox::indicator{{
        image: url(:/input/toggle-off.svg);
        width: {width}px;
        height: {height}px;
        max-width: {width}px;
        max-height: {height}px;
    }}

"""
CheckBoxTable = f"""
    QCheckBox {{
        color: {default};
        font-size: 16px;
        border-radius: 5px;
        margin-left: 50%;
    }}

    QCheckBox::indicator:checked {{
        image: url(:/input/toggle-on.svg);
        width: {width}px;
        height: {height}px;
        max-width: {width}px;
        max-height: {height}px;
    }}

    QCheckBox::indicator{{
        image: url(:/input/toggle-off.svg);
        width: {width}px;
        height: {height}px;
        max-width: {width}px;
        max-height: {height}px;
    }}

"""

CheckBoxSquare = f"""
    QCheckBox {{
        color: {default};
        font-size: 16px;
        border-radius: 5px;
    }}

    QCheckBox::indicator:checked {{
        image: url(:/input/toggle_square_on);
        width: {square_width}px;
        height: {square_height}px;
        max-width: {square_width}px;
        max-height: {square_height}px;
    }}

    QCheckBox::indicator{{
        image: url(:/input/toggle_square_off);
        width: {square_width}px;
        height: {square_height}px;
        max-width: {square_width}px;
        max-height: {square_height}px;
    }}


"""
settings_checkbox_width = 135  # width of the google button
settings_checkbox_height_ratio = 4  
SettingsCheckBox = f"""
    QCheckBox {{
        color: {default};
        font-size: 16px;
        border-radius: 5px;
        text-align: left center;
        width: {settings_checkbox_width}px;
        height: {settings_checkbox_width/settings_checkbox_height_ratio}px;
        max-width: {settings_checkbox_width}px;
        max-height: {settings_checkbox_width/settings_checkbox_height_ratio}px;
    }}

    QCheckBox::indicator:checked {{
        image: url(:/input/toggle_square_on);
        width: {settings_checkbox_width}px;
        height: {settings_checkbox_width/settings_checkbox_height_ratio}px;
        max-width: {settings_checkbox_width}px;
        max-height: {settings_checkbox_width/settings_checkbox_height_ratio}px;
    }}

    QCheckBox::indicator{{
        image: url(:/input/toggle_square_off);
        width: {settings_checkbox_width}px;
        height: {settings_checkbox_width/settings_checkbox_height_ratio}px;
        max-width: {settings_checkbox_width}px;
        max-height: {settings_checkbox_width/settings_checkbox_height_ratio}px;
        subcontrol-position: right center;
    }}
"""

WhiteEyeCheckBox = f"""
    QCheckBox {{
        color: {default};
        font-size: 16px;
        border-radius: 5px;
    }}

    QCheckBox::indicator:checked {{
        image: url(:/input/eye_white_open.svg);
        width: {square_width * (1/3)}px;
        height: {square_height * (2/3)}px;
        max-width: {square_width * (1/3)}px;
        max-height: {square_height * (2/3)}px;
    }}

    QCheckBox::indicator{{
        image: url(:/input/eye_white_closed.svg);
        width: {square_width * (1/3)}px;
        height: {square_height * (2/3)}px;
        max-width: {square_width * (1/3)}px;
        max-height: {square_height * (2/3)}px;
    }}
"""

BlackEyeCheckBox = f"""
    QCheckBox {{
        color: {default};
        font-size: 16px;
        border-radius: 5px;
    }}

    QCheckBox::indicator:checked {{
        image: url(:/input/eye_black_open.svg);
        width: {square_width * (1/3)}px;
        height: {square_height * (2/3)}px;
        max-width: {square_width * (1/3)}px;
        max-height: {square_height * (2/3)}px;
    }}

    QCheckBox::indicator{{
        image: url(:/input/eye_black_closed.svg);
        width: {square_width * (1/3)}px;
        height: {square_height * (2/3)}px;
        max-width: {square_width * (1/3)}px;
        max-height: {square_height * (2/3)}px;
    }}
"""
eye = "black" if not dark_mode_on else "white"
id = ""

EyeCheckBox = f"""
    QCheckBox{id} {{
        color: {default};
        font-size: 16px;
        border-radius: 5px;
    }}

    QCheckBox::indicator:checked {{
        image: url(:/input/eye_{eye}_open.svg);
        width: {square_width * (1/3)}px;
        height: {square_height * (2/3)}px;
        max-width: {square_width * (1/3)}px;
        max-height: {square_height * (2/3)}px;
    }}

    QCheckBox::indicator{{
        image: url(:/input/eye_{eye}_closed.svg);
        width: {square_width * (1/3)}px;
        height: {square_height * (2/3)}px;
        max-width: {square_width * (1/3)}px;
        max-height: {square_height * (2/3)}px;
    }}
"""
def custom_id(id):
    EyeCheckBox = f"""
        QCheckBox{id} {{
            color: {default};
            font-size: 16px;
            border-radius: 5px;
        }}

        QCheckBox{id}::indicator:checked {{
            image: url(:/input/eye_{eye}_open.svg);
            width: {square_width * (1/3)}px;
            height: {square_height * (2/3)}px;
            max-width: {square_width * (1/3)}px;
            max-height: {square_height * (2/3)}px;
        }}

        QCheckBox{id}::indicator{{
            image: url(:/input/eye_{eye}_closed.svg);
            width: {square_width * (1/3)}px;
            height: {square_height * (2/3)}px;
            max-width: {square_width * (1/3)}px;
            max-height: {square_height * (2/3)}px;
        }}
    """
    return EyeCheckBox

custom_eye = custom_id

