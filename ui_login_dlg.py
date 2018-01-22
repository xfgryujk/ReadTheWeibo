# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\login_dlg.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LoginDlg(object):
    def setupUi(self, LoginDlg):
        LoginDlg.setObjectName("LoginDlg")
        LoginDlg.setWindowModality(QtCore.Qt.ApplicationModal)
        LoginDlg.resize(382, 507)
        self.verticalLayout = QtWidgets.QVBoxLayout(LoginDlg)
        self.verticalLayout.setObjectName("verticalLayout")
        self.web_view = QtWebEngineWidgets.QWebEngineView(LoginDlg)
        self.web_view.setObjectName("web_view")
        self.verticalLayout.addWidget(self.web_view)

        self.retranslateUi(LoginDlg)
        QtCore.QMetaObject.connectSlotsByName(LoginDlg)

    def retranslateUi(self, LoginDlg):
        _translate = QtCore.QCoreApplication.translate
        LoginDlg.setWindowTitle(_translate("LoginDlg", "登录微博"))

from PyQt5 import QtWebEngineWidgets
