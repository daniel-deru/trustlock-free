# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './xml/apps_tab.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_apps_tab(object):
    def setupUi(self, apps_tab):
        apps_tab.setObjectName("apps_tab")
        apps_tab.resize(754, 526)
        apps_tab.setStyleSheet("QWidget {\n"
"    font-size: 16px;\n"
"    border-radius: 5px;\n"
"    padding: 5px 8px;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: white;\n"
"}\n"
"QLine {\n"
"    border-width: 1px;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(apps_tab)
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.hbox_open_apps_buttons = QtWidgets.QHBoxLayout()
        self.hbox_open_apps_buttons.setObjectName("hbox_open_apps_buttons")
        self.hbox_filter_widget = QtWidgets.QHBoxLayout()
        self.hbox_filter_widget.setObjectName("hbox_filter_widget")
        self.hbox_open_apps_buttons.addLayout(self.hbox_filter_widget)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hbox_open_apps_buttons.addItem(spacerItem)
        self.btn_delete = QtWidgets.QPushButton(apps_tab)
        self.btn_delete.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_delete.setObjectName("btn_delete")
        self.hbox_open_apps_buttons.addWidget(self.btn_delete)
        self.btn_add_app = QtWidgets.QPushButton(apps_tab)
        self.btn_add_app.setMinimumSize(QtCore.QSize(150, 0))
        self.btn_add_app.setMaximumSize(QtCore.QSize(150, 16777215))
        self.btn_add_app.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add_app.setObjectName("btn_add_app")
        self.hbox_open_apps_buttons.addWidget(self.btn_add_app)
        self.verticalLayout.addLayout(self.hbox_open_apps_buttons)
        self.hbox_apps_container = QtWidgets.QHBoxLayout()
        self.hbox_apps_container.setObjectName("hbox_apps_container")
        self.vbox_open_apps = QtWidgets.QVBoxLayout()
        self.vbox_open_apps.setObjectName("vbox_open_apps")
        self.lbl_open_apps = QtWidgets.QLabel(apps_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_open_apps.sizePolicy().hasHeightForWidth())
        self.lbl_open_apps.setSizePolicy(sizePolicy)
        self.lbl_open_apps.setMaximumSize(QtCore.QSize(16777215, 50))
        self.lbl_open_apps.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_open_apps.setObjectName("lbl_open_apps")
        self.vbox_open_apps.addWidget(self.lbl_open_apps)
        self.frame = QtWidgets.QFrame(apps_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMaximumSize(QtCore.QSize(16777215, 1))
        self.frame.setStyleSheet("background: #9ecd16;")
        self.frame.setFrameShape(QtWidgets.QFrame.HLine)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.vbox_open_apps.addWidget(self.frame)
        self.scrollArea = QtWidgets.QScrollArea(apps_tab)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 716, 409))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gbox_apps = QtWidgets.QGridLayout()
        self.gbox_apps.setObjectName("gbox_apps")
        self.verticalLayout_2.addLayout(self.gbox_apps)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.vbox_open_apps.addWidget(self.scrollArea)
        self.hbox_apps_container.addLayout(self.vbox_open_apps)
        self.verticalLayout.addLayout(self.hbox_apps_container)

        self.retranslateUi(apps_tab)
        QtCore.QMetaObject.connectSlotsByName(apps_tab)

    def retranslateUi(self, apps_tab):
        _translate = QtCore.QCoreApplication.translate
        apps_tab.setWindowTitle(_translate("apps_tab", "Form"))
        self.btn_delete.setText(_translate("apps_tab", "Bulk Delete"))
        self.btn_add_app.setText(_translate("apps_tab", "Add"))
        self.lbl_open_apps.setText(_translate("apps_tab", "Apps"))