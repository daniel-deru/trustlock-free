import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, button, green, dark_blue, light_blue, default, orange

ToolButton = f"""
    QToolButton {{
        background-color: transparent;
        border: none;
        border-radius: 5px;
        color: white;
    }}

"""