import os
import sys
import typing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QTabBar, QStylePainter, QStyleOptionTab, QStyle, QProxyStyle, QApplication, QWidget, QTabWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QRect, QPoint, pyqtSignal

from utils.helpers import set_font, StyleSheet

from widgetStyles.TabBar import TabBar as TabBarStyle
from widgetStyles.TabWidget import TabWidget


class TabBar(QTabBar):
    update_bar = pyqtSignal(bool)
    def __init__(self, parent: typing.Optional[QWidget] = ...) -> None:
        super().__init__(parent)
        self.setAutoFillBackground(True)
        set_font([self])
        self.read_style()
        self.update_bar.connect(self.read_style)
        
    def read_style(self):
        stylesheet = StyleSheet([TabBarStyle]).create()
        self.setStyleSheet(stylesheet)
        
    def tabSizeHint(self, index):
        s = QTabBar.tabSizeHint(self, index)
        s.transpose()
        return s

    def paintEvent(self, event):
        painter = QStylePainter(self)
        opt = QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QRect(QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QStyle.CE_TabBarTabLabel, opt);
            painter.restore()


class ProxyStyle(QProxyStyle):
    def drawControl(self, element, opt, painter, widget):
        if element == QStyle.CE_TabBarTabLabel:
            ic = self.pixelMetric(QStyle.PM_TabBarIconSize)
            r = QRect(opt.rect)
            w =  0 if opt.icon.isNull() else opt.rect.width() + self.pixelMetric(QStyle.PM_TabBarIconSize)
            r.setHeight(opt.fontMetrics.width(opt.text) + w)
            r.moveBottom(opt.rect.bottom())
            opt.rect = r
        QProxyStyle.drawControl(self, element, opt, painter, widget)

# if __name__ == '__main__':
#     import sys

#     app = QApplication(sys.argv)
        """
        This part is important
        """
#     QApplication.setStyle(ProxyStyle())
#     w = TabWidget()
#     w.addTab(QWidget(), QIcon("zoom.png"), "ABC")
#     w.addTab(QWidget(), QIcon("zoom-in.png"), "ABCDEFGH")
#     w.addTab(QWidget(), QIcon("zoom-out.png"), "XYZ")

#     w.resize(640, 480)
#     w.show()

#     sys.exit(app.exec_())