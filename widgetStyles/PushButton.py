import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, button, green, dark_blue, light_blue, default, orange

PushButton = f"""
    QPushButton {{
    background-color: {light_blue};
    color: white;
    border: 1px solid {light_blue};
    border-radius: 5px;
    font-size: 16px;
    padding: 5px 8px;
    max-width: 200px;
    min-width: 100px;
    min-height: 20px;
    max-height: 20px;
}}

QPushButton:pressed {{
    background-color: transparent;
    color: {default};
    border: 1px solid {light_blue};
}}
"""

PushButton100Width = f"""
    QPushButton {{
    background-color: {light_blue};
    color: white;
    border: 1px solid {light_blue};
    border-radius: 5px;
    font-size: 16px;
    padding: 5px 8px;
    max-width: 100px;
    min-width: 100px;
    min-height: 20px;
}}



QPushButton:pressed {{
    background-color: transparent;
    color: {default};
    border: 1px solid {light_blue};
}}
"""

ButtonBackIcon = f"""
    QPushButton#btn_back {{
    background-color: transparent;
    text-align: left;
    max-width: 45px;
    min-width: 45px;
    width: 45px;
    height: 45px;
    border: none;
}}
"""

ButtonFullWidth = f"""
    QPushButton {{
    background-color: {light_blue};
    color: white;
    border: 1px solid {light_blue};
    border-radius: 5px;
    font-size: 16px;
    padding: 5px 8px;
    min-width: 100px;
    max-width: 250px;
}}

QPushButton:pressed {{
    background-color: transparent;
    color: {default};
    border: 1px solid {light_blue};
}}
"""

ForgotPasswordButton = f"""
    QPushButton#btn_forgot_password {{
        max-width: 1000px;
    }}
"""

VaultButton = f"""
QPushButton {{
    background-color: {light_blue};
    color: white;
    border: 1px solid {light_blue};
    border-radius: 5px;
    font-size: 16px;
    padding: 5px 8px;
    max-width: 150px;
    min-width: 150px;
}}

QPushButton:pressed {{
    background-color: transparent;
    color: {default};
    border: 1px solid {light_blue};
}}
"""
VaultButtonLeftAlign = f"""
QPushButton {{
    background-color: {light_blue};
    color: white;
    border: 1px solid {light_blue};
    border-radius: 5px;
    font-size: 16px;
    padding: 5px 8px;
    max-width: 150px;
    min-width: 150px;
    text-align: left;
}}

QPushButton:pressed {{
    background-color: transparent;
    color: {default};
    border: 1px solid {light_blue};
}}
"""

IconButton = f"""
    QPushButton {{
    background-color: {light_blue};
    border: none;
    border-radius: 5px;
    width: 125px;
    min-height: 25px;
}}

QPushButton:pressed {{
    border: none;
    background-color: {green};
}}
"""

IconToolButton = f"""
    QToolButton {{
    background-color: {light_blue};
    border: none;
    border-radius: 5px;
    width: 70px;
    height: 30px;
}}

QPushButton:pressed {{
    border: none;
    background-color: {green};
}}
"""

def _create_custom_tool_button(id=""):
    IconToolButton = f"""
        QToolButton{id} {{
        background-color: {light_blue};
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 16px;
        width: 70px;
        height: 30px;
    }}

    QPushButton:pressed {{
        border: none;
        background-color: {green};
    }}
    """
    
    return IconToolButton

def _create_vault_button(color=light_blue):
    VaultButtonLeftAlign = f"""
        QPushButton {{
            background-color: {color};
            color: white;
            border: 1px solid {color};
            border-radius: 5px;
            font-size: 16px;
            padding: 5px 8px;
            max-width: 275px;
            min-width: 100px;
            text-align: left;
        }}

        QPushButton:pressed {{
            background-color: transparent;
            color: transparent;
            border: 1px solid {color};
        }}
        """
    return VaultButtonLeftAlign

def _create_link(id: str = ""):
    return f"""
        QPushButton{id} {{
            background: transparent;
            color: {default};
            border: none;
            width: 75px;
            }}

        QPushButton:hover {{
            color: blue;
            text-decoration: underline;
        }}
    """
    
PushButtonLink = _create_link
VaultButton = _create_vault_button
IconToolButton = _create_custom_tool_button