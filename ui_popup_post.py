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
        PopupPost.setEnabled(True)
        PopupPost.resize(367, 230)
        PopupPost.setWindowOpacity(0.0)
        PopupPost.setAutoFillBackground(False)
        PopupPost.setStyleSheet("#centralwidget {\n"
"    border-image: url(:/image/bg.png) 30 repeat;\n"
"    border: 30;\n"
"}\n"
"")
        self.centralwidget = QtWidgets.QWidget(PopupPost)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(15, 15, 15, 15)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setSpacing(7)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.close_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.close_button.sizePolicy().hasHeightForWidth())
        self.close_button.setSizePolicy(sizePolicy)
        self.close_button.setMinimumSize(QtCore.QSize(30, 30))
        self.close_button.setMaximumSize(QtCore.QSize(30, 30))
        self.close_button.setBaseSize(QtCore.QSize(0, 0))
        self.close_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.close_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.close_button.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.close_button.setStyleSheet("")
        self.close_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/image/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.close_button.setIcon(icon)
        self.close_button.setFlat(True)
        self.close_button.setObjectName("close_button")
        self.horizontalLayout.addWidget(self.close_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.content_widget = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.content_widget.sizePolicy().hasHeightForWidth())
        self.content_widget.setSizePolicy(sizePolicy)
        self.content_widget.setObjectName("content_widget")
        self.verticalLayout.addWidget(self.content_widget)
        PopupPost.setCentralWidget(self.centralwidget)

        self.retranslateUi(PopupPost)
        self.close_button.clicked.connect(PopupPost.close)
        QtCore.QMetaObject.connectSlotsByName(PopupPost)

    def retranslateUi(self, PopupPost):
        _translate = QtCore.QCoreApplication.translate
        PopupPost.setWindowTitle(_translate("PopupPost", "微博"))
        self.label.setText(_translate("PopupPost", "ReadTheWeibo"))

import res_rc
