import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default
import assets.resources

RadioButton = f"""
    QRadioButton {{
        color: {default};
        font-size: 16px;
    }}

    QRadioButton::indicator:checked {{
        image: url(:/input/radio-on.svg);
        max-height: 20px;
        max-width: 20px;
        height: 20px;
        width: 20px;
    }}

    QRadioButton::indicator:unchecked {{
        image: url(:/input/radio-off.svg);
        max-height: 20px;
        max-width: 20px;
        height: 20px;
        width: 20px;
    }}
"""