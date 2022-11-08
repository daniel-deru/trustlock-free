# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './xml/backup_verify.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_backup_verify(object):
    def setupUi(self, backup_verify):
        backup_verify.setObjectName("backup_verify")
        backup_verify.resize(400, 346)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(backup_verify)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lbl_warning = QtWidgets.QLabel(backup_verify)
        self.lbl_warning.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_warning.setObjectName("lbl_warning")
        self.verticalLayout_3.addWidget(self.lbl_warning)
        self.lbl_heading = QtWidgets.QLabel(backup_verify)
        self.lbl_heading.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_heading.setObjectName("lbl_heading")
        self.verticalLayout_3.addWidget(self.lbl_heading)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lbl_explain = QtWidgets.QLabel(backup_verify)
        self.lbl_explain.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lbl_explain.setWordWrap(True)
        self.lbl_explain.setObjectName("lbl_explain")
        self.horizontalLayout_2.addWidget(self.lbl_explain)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lbl_reccomend = QtWidgets.QLabel(backup_verify)
        self.lbl_reccomend.setWordWrap(True)
        self.lbl_reccomend.setObjectName("lbl_reccomend")
        self.horizontalLayout.addWidget(self.lbl_reccomend)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lbl_liability = QtWidgets.QLabel(backup_verify)
        self.lbl_liability.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lbl_liability.setObjectName("lbl_liability")
        self.horizontalLayout_3.addWidget(self.lbl_liability)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_keys = QtWidgets.QLabel(backup_verify)
        self.lbl_keys.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_keys.setObjectName("lbl_keys")
        self.verticalLayout.addWidget(self.lbl_keys)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btn_yes = QtWidgets.QPushButton(backup_verify)
        self.btn_yes.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_yes.setObjectName("btn_yes")
        self.horizontalLayout_4.addWidget(self.btn_yes)
        self.btn_no = QtWidgets.QPushButton(backup_verify)
        self.btn_no.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_no.setObjectName("btn_no")
        self.horizontalLayout_4.addWidget(self.btn_no)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.retranslateUi(backup_verify)
        QtCore.QMetaObject.connectSlotsByName(backup_verify)

    def retranslateUi(self, backup_verify):
        _translate = QtCore.QCoreApplication.translate
        backup_verify.setWindowTitle(_translate("backup_verify", "Are you sure?"))
        self.lbl_warning.setText(_translate("backup_verify", "Warning!"))
        self.lbl_heading.setText(_translate("backup_verify", "Please Read"))
        self.lbl_explain.setText(_translate("backup_verify", "1) Without your keys you cannot restore your account incase of losing access to your device or data etc."))
        self.lbl_reccomend.setText(_translate("backup_verify", "2) Do not save your keys inside Trust Lock. It is reccomended to write the keys down and keep in a safe place."))
        self.lbl_liability.setText(_translate("backup_verify", "Smart MetaTec does not take responsibilty for any data loss."))
        self.lbl_keys.setText(_translate("backup_verify", "Did you save your keys in a safe place?"))
        self.btn_yes.setText(_translate("backup_verify", "Yes"))
        self.btn_no.setText(_translate("backup_verify", "No"))
