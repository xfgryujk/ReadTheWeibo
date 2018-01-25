# -*- coding: utf-8 -*-

from logging import getLogger

from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtWidgets import QMainWindow, QApplication

from ui_popup_post import Ui_PopupPost

logger = getLogger(__name__)


class PopupPost(QMainWindow, Ui_PopupPost):

    def __init__(self, read_the_weibo):
        super().__init__()
        self.setupUi(self)

        self._read_the_weibo = read_the_weibo

    def setupUi(self, popup_post):
        super().setupUi(popup_post)
        self.setWindowFlags(Qt.ToolTip
                            | Qt.FramelessWindowHint
                            | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        desktop = QApplication.desktop()
        self.move(desktop.width() - self.width() - 50,
                  desktop.height() - self.height() - 300)

        # 淡出淡入动画
        self._fade_anim = QPropertyAnimation(self, b'windowOpacity', self)
        self._fade_anim.setDuration(300)
        self._fade_anim.setStartValue(0)
        self._fade_anim.setEndValue(0.8)
        self._fade_anim.finished.connect(self._on_anim_finish)

    def show_post(self, post):
        """
        显示一条微博
        :param post: 微博
        """

        user = post['user']['screen_name']
        content = post['text']

        # TODO UI换成浏览器
        self.content_view.setText('{}：{}'.format(user, content))

        # 淡入
        self._fade_anim.setDirection(QPropertyAnimation.Forward)
        self._fade_anim.start()
        self.show()

        # TODO 如果只弹窗不发声则过一段时间自动关闭

    def closeEvent(self, event):
        """
        取消关闭事件，改成淡出、隐藏窗口
        """

        logger.debug('closeEvent')
        event.ignore()

        if (self._fade_anim.state() != QPropertyAnimation.Running
            or self._fade_anim.direction() != QPropertyAnimation.Backward):
            self._read_the_weibo.on_popup_post_close()

            # 淡出
            self._fade_anim.setDirection(QPropertyAnimation.Backward)
            self._fade_anim.start()
            self._fade_anim.setCurrentTime(self._fade_anim.totalDuration())

    def _on_anim_finish(self):
        if self._fade_anim.direction() == QPropertyAnimation.Backward:
            logger.debug('_on_anim_finish, direction = Backward')
            self.hide()
            self._read_the_weibo.on_popup_post_hide()
        else:
            logger.debug('_on_anim_finish, direction = Forward')
