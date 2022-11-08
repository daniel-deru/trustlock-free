import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default, light_blue


SpinBox = f"""
    QSpinBox {{
        background-color: {mode};
        color: {default};
        font-size: 16px;
        padding: 5px 8px;
        border-radius: 5px;
        border: 1px solid {light_blue};
    }}

    QSpinBox::down-button {{
        border: none;
        border-left: 1px solid {light_blue};
        image: url(:/arrows/down-arrow.svg);
        margin-top: 2px;
        width: 15px;
        height: 15px;
        padding: 0px 5px;
        background-color: {mode};
        border-bottom-right-radius: 5px;
        border-bottom-left-radius: 0px;
    }}

    QSpinBox::up-button:pressed {{
        background-color: {mode};
    }}

    QSpinBox::up-button {{
        border: none;
        border-left: 1px solid {light_blue};
        image: url(:/arrows/up-arrow.svg);
        width: 15px;
        height: 15px;
        padding: 0px 5px;
        margin-bottom: 2px;
        background-color: {mode};
        border-top-right-radius: 5px;
    }}

    QSpinBox::down-button:pressed {{
        background-color: {mode};
    }}

"""