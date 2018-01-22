# -*- coding: utf-8 -*-

from logging import getLogger

from PyQt5.QtWidgets import QMainWindow, QApplication

from ui_popup_post import Ui_PopupPost

logger = getLogger(__name__)


class PopupPost(QMainWindow, Ui_PopupPost):

    def __init__(self, read_the_weibo):
        super().__init__()
        self.setupUi(self)

        self._read_the_weibo = read_the_weibo

    def closeEvent(self, event):
        logger.debug('closeEvent')
        event.ignore()
        self.hide()
        self._read_the_weibo.on_popup_post_close()

    def show_post(self, post):
        """
        显示一条微博
        :param post: 微博
        """

        desktop = QApplication.desktop()
        self.move(desktop.width() - self.width() - 50,
                  desktop.height() - self.height() - 300)

        user = post['user']['screen_name']
        content = post['text']

        # 测试用的简易UI
        self.label.setText('{}：{}'.format(user, content))

        self.show()

        # TODO 如果只弹窗不发声则过一段时间自动关闭
