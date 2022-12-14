# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './xml/download_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DownloadDialog(object):
    def setupUi(self, DownloadDialog):
        DownloadDialog.setObjectName("DownloadDialog")
        DownloadDialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(DownloadDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.lbl_message = QtWidgets.QLabel(DownloadDialog)
        self.lbl_message.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_message.setObjectName("lbl_message")
        self.verticalLayout.addWidget(self.lbl_message)
        self.lbl_no_close = QtWidgets.QLabel(DownloadDialog)
        self.lbl_no_close.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_no_close.setObjectName("lbl_no_close")
        self.verticalLayout.addWidget(self.lbl_no_close)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.bar_download = QtWidgets.QProgressBar(DownloadDialog)
        self.bar_download.setProperty("value", 0)
        self.bar_download.setObjectName("bar_download")
        self.verticalLayout.addWidget(self.bar_download)

        self.retranslateUi(DownloadDialog)
        QtCore.QMetaObject.connectSlotsByName(DownloadDialog)

    def retranslateUi(self, DownloadDialog):
        _translate = QtCore.QCoreApplication.translate
        DownloadDialog.setWindowTitle(_translate("DownloadDialog", "Downloading"))
        self.lbl_message.setText(_translate("DownloadDialog", "Connecting to server."))
        self.lbl_no_close.setText(_translate("DownloadDialog", "Please do not close this window."))
