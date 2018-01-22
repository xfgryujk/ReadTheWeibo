# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow

from ui_mainwindow import Ui_MainWindow
from read_the_weibo import ReadTheWeibo


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.read_the_weibo = ReadTheWeibo()

    def closeEvent(self, event):
        self.read_the_weibo.save_weibo()
