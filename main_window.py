# -*- coding: utf-8 -*-

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMainWindow

from read_the_weibo import ReadTheWeibo
from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.read_the_weibo = ReadTheWeibo()
        self.read_the_weibo.start()

    def closeEvent(self, event):
        self.read_the_weibo.stop()
        self.read_the_weibo.save_session()
        QCoreApplication.quit()
