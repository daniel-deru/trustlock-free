from widgetStyles.styles import default, mode, button, color, dark_blue, light_blue, green
import assets.resources

ScrollArrea = f"""
    QScrollArea {{
        background-color: {mode};
        margin: 0px;
        padding: 0px;
        border-radius: 5px;
        border: 1px solid {light_blue};
    }}
    
    QScrollArea QWidget {{
        background-color: {mode};
        border-radius: 5px;
    }}

"""

ScrollAreaGroups = f"""
    QScrollArea {{
        background-color: {mode};
        margin: 0px;
        padding: 0px;
        border-radius: 5px;
    }}
    
    QScrollArea QWidget {{
        background-color: {mode};
        border-radius: 5px;
    }}

"""