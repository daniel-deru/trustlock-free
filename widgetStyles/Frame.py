import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default, light_blue

from widgetStyles.styles import dark_grey, light_grey

Frame = f"""
    QFrame {{
        font-size: 16px;
        border-radius: 5px;
        font-size: 16px;
        padding: 0px;
        background-color: {mode};
        color: {default};
        border: 1px solid {light_blue};
    }}
"""

TodoFrameDelete = f"""
        QFrame {{
        font-size: 16px;
        border-radius: 5px;
        font-size: 16px;
        background-color: #00A62E;
        color: #ffffff;
        max-height: 100px;
        height: 100px;
        padding: 0px;
    }}
"""

TodoFrameComplete = f"""
    QFrame {{
        font-size: 16px;
        border-radius: 5px;
        font-size: 16px;
        background-color: #A60000;
        color: #ffffff;
        max-height: 100px;
        height: 100px;
        padding: 0px;
    }}
"""

def create_todo_frame(status):
    TodoFrameComplete = f"""
        QFrame {{
            font-size: 16px;
            border-radius: 5px;
            font-size: 16px;
            background-color: {status};
            color: #ffffff;
            max-height: 100px;
            height: 100px;
            padding: 0px;
        }}
    """
    return TodoFrameComplete

def vault_type_frame(id: str, color: str):
    return f"""
        QFrame{id} {{
            border-radius: 10px;
            border: 2px solid {color};
        }}
    """


def create_frame(id, dark_mode):
    PassGenFrame = f"""
        QFrame{id}{{
            border-radius: 10px;
            background: {dark_grey if dark_mode else light_grey};
        }}
    """
    return PassGenFrame

PassGenFrame = create_frame
FrameContainer = create_frame
TodoFrame = create_todo_frame