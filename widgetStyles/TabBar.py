import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default, button, green, orange, light_blue, dark_blue


TabBar = f"""
    QTabBar{{
        background-color: {green};
        border: none;
        qproperty-drawBase: 0;
    }}
    QTabBar::tab {{
        height: 100px;
        padding: 10px;
        border: none;
        background-color: {green};
        color: black;
        font-size: 16px;
    }}

        QTabBar::tab:selected {{
        background: {mode};
        color: {default};    
    }}
"""

RegisterTabBar = f"""
    QTabBar{{
        border: none;
        qproperty-drawBase: 0;
    }}
    QTabBar::tab {{
        padding: 5px;
        border: none;
        color: {default};
        font-size: 16px;
        width: 100px;
        height: 30px;
    }}

    QTabBar::tab:selected {{
        color: {light_blue};
        border-bottom: 1px solid {light_blue};  
    }}

"""