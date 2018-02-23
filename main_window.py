# -*- coding: utf-8 -*-

import json
from logging import getLogger

from PyQt5.QtCore import Qt, QCoreApplication, QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QSystemTrayIcon

from read_the_weibo import ReadTheWeibo
from ui_mainwindow import Ui_MainWindow

logger = getLogger(__name__)

SETTINGS_PATH = 'data/settings.json'


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__(None, Qt.WindowMinimizeButtonHint
                         | Qt.WindowCloseButtonHint
                         | Qt.MSWindowsFixedSizeDialogHint)
        self.setupUi(self)

        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon(':/icon/sina.ico'))
        self.tray.setToolTip('ReadTheWeibo')
        self.tray.activated.connect(self._on_tray_activate)

        self.read_the_weibo = ReadTheWeibo(self)
        self.load_settings()
        self.read_the_weibo.start()

    def setupUi(self, main_window):
        super().setupUi(main_window)
        self.setFixedSize(self.width(), self.height())

        self.speak_check.stateChanged.connect(self._on_speak_check_change)
        self.show_check.stateChanged.connect(self._on_show_check_change)

    def closeEvent(self, event):
        self.read_the_weibo.stop()
        self.read_the_weibo.save_session()
        self.save_settings()
        QCoreApplication.quit()

    def load_settings(self):
        try:
            with open(SETTINGS_PATH) as f:
                settings = json.load(f)
                self.speak_check.setChecked(settings['speak_post'])
                self.show_check.setChecked(settings['show_post'])
        except OSError:  # 打开文件错误
            pass
        except KeyError:
            pass
        except json.JSONDecodeError:
            logger.exception('读取设置时出错：')

    def save_settings(self):
        try:
            settings = {
                'speak_post': self.speak_check.isChecked(),
                'show_post':  self.show_check.isChecked(),
            }
            with open(SETTINGS_PATH, 'w') as f:
                json.dump(settings, f, indent=4)
        except OSError:  # 打开文件错误
            pass

    def changeEvent(self, event):
        # 最小化到托盘
        if (event.type() == QEvent.WindowStateChange
           and int(self.windowState()) & Qt.WindowMinimized):
            self.hide()
            self.tray.show()

    def _on_tray_activate(self, reason):
        # 单击托盘时恢复窗口
        if reason == QSystemTrayIcon.Trigger:
            self.show()
            self.setWindowState(Qt.WindowState((int(self.windowState())
                                               & ~Qt.WindowMinimized)
                                               | Qt.WindowActive))
            self.tray.hide()

    def _on_speak_check_change(self, state):
        self.read_the_weibo.speak_post = state != Qt.Unchecked

    def _on_show_check_change(self, state):
        self.read_the_weibo.show_post = state != Qt.Unchecked
