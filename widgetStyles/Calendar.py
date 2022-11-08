import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default, button, light_blue
import assets.resources


Calendar = f"""
QCalendarWidget {{
    border: 1px solid {light_blue};
}}
QCalendarWidget QToolButton {{
  	height: 40px;
  	width: 100px;
  	color: {button};
  	font-size: 16px;
  	icon-size: 37px, 37px;
  	background-color: {light_blue};
  }}


  QCalendarWidget QWidget#qt_calendar_prevmonth {{
      qproperty-icon: url(:/arrows/left-arrow.svg);
      background-color: {mode};
      border-left: 1px solid {light_blue};
      border-top: 1px solid {light_blue}
  }}
  QCalendarWidget QWidget#qt_calendar_nextmonth {{
      qproperty-icon: url(:/arrows/right-arrow.svg);
      background-color: {mode};
      border-right: 1px solid {light_blue};
      border-top: 1px solid {light_blue}
  }}


  QCalendarWidget QMenu {{
  	width: 100px;
  	left: 20px;
  	color: {color};
  	font-size: 12px;
  	background-color: {mode};
  }}

  QCalendarWidget QSpinBox {{ 
  	width: 100px; 
  	font-size:16px; 
  	color: {light_blue}; 
  	background-color: {mode}; 
  	selection-background-color: {light_blue};
  	selection-color: {button};
  }}

    QCalendarWidget QSpinBox::up-button {{ 
        subcontrol-origin: border;  
        subcontrol-position: top right;  
        image: url(:/arrows/up-arrow.svg);
        width: 30px;
        height: 30px; 
    }}

    QCalendarWidget QSpinBox::down-button {{
        subcontrol-origin: border; 
        subcontrol-position: bottom right;  
        image: url(:/arrows/down-arrow.svg);
        width: 30px;  
        height: 30px; 
    }}

    QCalendarWidget QSpinBox::up-arrow {{ 
        width: 10px;  
        height: 10px; 
    }}

    QCalendarWidget QSpinBox::down-arrow {{ 
        width: 10px;  
        height: 10px;
    }}
   

    QCalendarWidget QWidget {{ 
        alternate-background-color: {mode};
        }}
   
    QCalendarWidget QAbstractItemView:enabled {{
        font-size: 16px;  
        color: {light_blue};  
        background-color: {mode};  
        selection-background-color: {light_blue}; 
        selection-color: {button};
        outline: none;
        padding: 10px;
        border-bottom: 2px solid {light_blue};
        border-left: 1px solid {light_blue};
        border-right: 1px solid {light_blue};

    }}
   

    QCalendarWidget QAbstractItemView:disabled {{ 
        color: {color}; 
    }}
"""