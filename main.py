# -*- coding: utf-8 -*-

import logging
import sys

from PyQt5.QtWidgets import QApplication

# noinspection PyUnresolvedReferences
import res_rc  # 注册资源
from main_window import MainWindow

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)-15s [%(name)s] %(levelname)s: %(message)s')


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
