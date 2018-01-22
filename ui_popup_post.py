# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\popup_post.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PopupPost(object):
    def setupUi(self, PopupPost):
        PopupPost.setObjectName("PopupPost")
        PopupPost.resize(437, 219)
        PopupPost.setWindowTitle("")
        PopupPost.setWindowOpacity(1.0)
        self.centralwidget = QtWidgets.QWidget(PopupPost)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setOpenExternalLinks(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        PopupPost.setCentralWidget(self.centralwidget)

        self.retranslateUi(PopupPost)
        QtCore.QMetaObject.connectSlotsByName(PopupPost)

    def retranslateUi(self, PopupPost):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("PopupPost", "TextLabel"))

