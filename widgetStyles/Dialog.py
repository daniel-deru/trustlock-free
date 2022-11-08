import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default

Dialog = f"""
    QDialog {{
        background-color: {mode};
        font-size: 16px;
    }}
"""