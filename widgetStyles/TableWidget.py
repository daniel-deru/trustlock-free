import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default, button, green

TableWidget = f"""
    QWidget {{
        padding: 0px;
    }}
    QTableWidget {{
        border: none;
        padding: 0px;
        gridline-color: {default};
        outline: 0;
    }}
    QHeaderView {{
        qproperty-defaultAlignment: AlignHCenter AlignVCenter;
        background-color: {green};
    }}
    
    QHeaderView::section {{
        padding: 5px;
        background-color: {green};
        color: {default};
        border: none;
    }}
    
    QTableWidget::item {{
        color: {default};
        background-color: {mode};
    }}
    
    QTableWidget::item:focus {{
        border: 0px;
        background-color: {green};
        color: {button};
    }}
 
    QTableCornerButton::section {{
        background-color: {green};
    }}
    
    QScrollBar:vertical {{
      width: 10px;
    }}
    
    QScrollBar::handle:vertical {{
        min-height: 10px;
        background-color: {green};
    }}

    QScrollBar::add-line:vertical {{
        background: none;
    }}

    QScrollBar::sub-line:vertical {{
        background: none;
    }}
"""
TableWidget2 = f"""
    QWidget {{
        padding: 0px;
    }}
    QTableWidget {{
        border: none;
        padding: 0px;
        gridline-color: {color};
        outline: 0;
    }}
    QHeaderView {{
        qproperty-defaultAlignment: AlignHCenter AlignVCenter;
    }}
    QHeaderView::section {{
        padding: 5px;
        background-color: {color};
        color: {button};
        border: none;
    }}

    QTableWidget::item {{
        color: {default};
    }}

    QTableWidget::item:focus {{
        border: 0px;
        background-color: {color};
        color: {button};
    }}
 
    QTableWidget QTableCornerButton::section {{
        background-color: {green};
    }}
"""