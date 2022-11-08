from widgetStyles.styles import default, mode, button, color, dark_blue, light_blue, green
import assets.resources

ComboBox = f"""
    QComboBox {{
        color: {default};
        border: 1px solid {light_blue};
        background-color: {mode};
        border-radius: 5px;
        font-size: 16px;
        min-height: 30px;
    }}

    QComboBox::drop-down {{
        width: 40px;
        background-color: {mode};
        border-radius: 5px;
 
    }}

    QComboBox QAbstractItemView {{
        background-color: {mode};
        selection-background-color: {green};
        selection-color: {default};
        color: {default};
        outline: none;
        padding: 0px;
        border: 1px solid {light_blue};
    }}
    
    QComboBox QAbstractItemView::item {{
        min-height: 35px;
        font-size: 16px;
    }}
    
    QComboBox QAbstractItemView::item:selected {{
        background-color: {green};
        color: black;
    }}
    
    QComboBox QAbstractItemView::item:hover {{
        background-color: {green};
        color: black;
    }}
    
    QComboBox::down-arrow{{
        width: 15px;
        height: 15px;
        background-color: transparent;
        image: url(:/arrows/down-arrow.svg);
        border-radius: 5px;
    }} 
"""

ComboBoxFilter = f"""
    QComboBox {{
        color: {default};
        border: 1px solid {light_blue};
        background-color: {mode};
        border-radius: 5px;
        font-size: 16px;
        min-height: 20px;
        min-width: 150px;
        width: 258px;
    }}

    QComboBox::drop-down {{
        width: 40px;
        background-color: {mode};
        border-radius: 5px;
 
    }}

    QComboBox QAbstractItemView {{
        background-color: {mode};
        selection-background-color: {green};
        selection-color: {default};
        color: {default};
        outline: none;
        padding: 0px;
        border: 1px solid {light_blue};
    }}
    
    QComboBox QAbstractItemView::item {{
        min-height: 35px;
        font-size: 16px;
    }}
    
    QComboBox QAbstractItemView::item:selected {{
        background-color: {green};
        color: black;
    }}
    
    QComboBox QAbstractItemView::item:hover {{
        background-color: {green};
        color: black;
    }}
    
    QComboBox::down-arrow{{
        width: 15px;
        height: 15px;
        background-color: transparent;
        image: url(:/arrows/down-arrow.svg);
        border-radius: 5px;
    }} 
"""