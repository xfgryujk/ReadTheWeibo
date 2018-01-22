# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication

from main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    if not main_window.read_the_weibo.weibo.is_login():
        return
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
