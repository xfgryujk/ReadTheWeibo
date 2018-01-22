# -*- coding: utf-8 -*-

import logging

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QDialog

from ui_login_dlg import Ui_LoginDlg
from weibo import Weibo

logger = logging.getLogger(__name__)


class LoginDlg(QDialog, Ui_LoginDlg):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 微博的登录凭证cookie
        self._weibo_cookies = {}

        cookie_store = self.web_view.page().profile().cookieStore()
        cookie_store.deleteAllCookies()
        cookie_store.cookieAdded.connect(self._on_cookie_added)
        self.web_view.load(QUrl('https://passport.weibo.cn/signin/login'))

    def _on_cookie_added(self, cookie):
        if cookie.name() == b'SUB':
            try:
                cookie_sub = cookie.value().data().decode()
                cookies = {'SUB': cookie_sub}
                if Weibo(cookies).is_login():
                    self._weibo_cookies = cookies
                    self.accept()
                else:
                    logger.debug('无效的Cookie：%s', cookie_sub)

            except:
                logger.exception('获取登录状态时出错：')

    @property
    def weibo_cookies(self):
        """
        :return: dict，微博的登录凭证cookie，为空则未登录
        """

        return self._weibo_cookies
