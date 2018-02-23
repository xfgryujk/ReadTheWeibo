# -*- coding: utf-8 -*-

import json
from io import StringIO
from logging import getLogger

from PyQt5.QtCore import (Qt, QUrl, QPropertyAnimation,
                          QParallelAnimationGroup, QTimer)
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QApplication

from ui_popup_post import Ui_PopupPost

logger = getLogger(__name__)

POPUP_POST_HTML_URL = QUrl('file:///ui/web/popup_post.html')


class WeiboWebPage(QWebEnginePage):

    def acceptNavigationRequest(self, url, navigation_type, is_main_frame):
        if url == POPUP_POST_HTML_URL:
            return True
        # 在外部浏览器打开链接
        QDesktopServices.openUrl(url)
        return False


class WeiboWebView(QWebEngineView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('')
        self.setWindowFlags(Qt.ToolTip
                            | Qt.FramelessWindowHint
                            | Qt.WindowStaysOnTopHint)
        self.setPage(WeiboWebPage(self))

        self.load(POPUP_POST_HTML_URL)
        # 等待加载结束
        self._is_loading = True
        self.loadFinished.connect(self._on_load_finish)
        while self._is_loading:
            QApplication.processEvents()

    def _on_load_finish(self):
        self._is_loading = False
        self.loadFinished.disconnect(self._on_load_finish)

    def contextMenuEvent(self, event):
        # 去掉右键菜单
        pass

    @staticmethod
    def _get_post_dict(post):
        return {
            'id':           post.id,
            'userId':       post.user_id,
            'userName':     post.user_name,
            'avatarUrl':    post.avatar_url,
            'createTime':   int(post.create_time.timestamp() * 1000),
            'rawContent':   post.raw_content,
            'images':       [{
                                'previewUrl': i['preview_url'],
                                'largeUrl':   i['large_url']
                              } for i in post.images],
            'originalPost': (WeiboWebView._get_post_dict(post.original_post)
                             if post.is_repost else None)
        }

    def show_post(self, post):
        js = StringIO()
        js.write('showPost(')
        json.dump(self._get_post_dict(post), js)
        js.write(')')
        self.page().runJavaScript(js.getvalue())

        self.show()


class PopupPost(QMainWindow, Ui_PopupPost):

    def __init__(self, read_the_weibo):
        super().__init__(None, Qt.ToolTip
                         | Qt.FramelessWindowHint
                         | Qt.WindowStaysOnTopHint)
        self.setupUi(self)

        self._close_timer = QTimer(self)
        self._close_timer.setSingleShot(True)
        self._close_timer.timeout.connect(self.close)

        self._read_the_weibo = read_the_weibo

    def setupUi(self, popup_post):
        super().setupUi(popup_post)
        self.setAttribute(Qt.WA_TranslucentBackground)

        desktop = QApplication.desktop()
        self.move(desktop.width() - 50 - self.width(),
                  desktop.height() - 300 - self.height())

        # 因为带浏览器的透明窗口不能渲染，浏览器放在独立窗口
        self.content_view = WeiboWebView(self)
        self.content_view.setWindowOpacity(0)

        # 淡出淡入动画
        self._window_fade_anim = QPropertyAnimation(self, b'windowOpacity', self)
        self._window_fade_anim.setDuration(300)
        self._window_fade_anim.setStartValue(0)
        self._window_fade_anim.setEndValue(0.5)
        self._content_fade_anim = QPropertyAnimation(self.content_view, b'windowOpacity', self)
        self._content_fade_anim.setDuration(300)
        self._content_fade_anim.setStartValue(0)
        self._content_fade_anim.setEndValue(0.7)
        self._fade_anim_group = QParallelAnimationGroup(self)
        self._fade_anim_group.addAnimation(self._window_fade_anim)
        self._fade_anim_group.addAnimation(self._content_fade_anim)
        self._fade_anim_group.finished.connect(self._on_anim_finish)

    def moveEvent(self, event):
        logger.debug('moveEvent')
        # 如果在这里更新，content_widget位置和尺寸不对
        QTimer.singleShot(0, self._update_content_view_geometry)

    def resizeEvent(self, event):
        logger.debug('resizeEvent')
        # 如果在这里更新，content_widget位置和尺寸不对
        QTimer.singleShot(0, self._update_content_view_geometry)

    def _update_content_view_geometry(self):
        pos = self.mapToGlobal(self.content_widget.pos())
        size = self.content_widget.size()
        logger.debug('content_widget: (%d, %d) %d x %d', pos.x(), pos.y(), size.width(), size.height())
        self.content_view.setGeometry(pos.x(), pos.y(), size.width(), size.height())

    def show_post(self, post):
        """
        显示一条微博
        :param post: 微博
        """

        self.show()
        self.content_view.show_post(post)

        # 淡入
        self._fade_anim_group.setDirection(QPropertyAnimation.Forward)
        self._fade_anim_group.start()

        # 如果只弹窗不发声则过一段时间自动关闭
        if not self._read_the_weibo.speak_post:
            self._close_timer.start(int(len(post.content) * 0.33 * 1000))

    def closeEvent(self, event):
        """
        取消关闭事件，改成淡出、隐藏窗口
        """

        logger.debug('closeEvent')
        event.ignore()
        self._close_timer.stop()

        if (self._fade_anim_group.state() != QPropertyAnimation.Running
            or self._fade_anim_group.direction() != QPropertyAnimation.Backward):
            self._read_the_weibo.on_popup_post_close()

            # 淡出
            self._fade_anim_group.setDirection(QPropertyAnimation.Backward)
            self._fade_anim_group.start()

    def _on_anim_finish(self):
        if self._fade_anim_group.direction() == QPropertyAnimation.Backward:
            logger.debug('_on_anim_finish, direction = Backward')
            self.content_view.hide()
            self.hide()
            self._read_the_weibo.on_popup_post_hide()
        else:
            logger.debug('_on_anim_finish, direction = Forward')
