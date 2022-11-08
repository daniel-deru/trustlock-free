import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default, green

TabWidget = f"""
    QTabWidget {{
        background-color: {mode};
        border: none;
    }}

    QTabWidget::pane {{
        background-color: {color};
    }}

    QTabWidget::tab-bar {{
        background-color: {green};
    }}
"""