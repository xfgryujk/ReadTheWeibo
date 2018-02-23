# -*- coding: utf-8 -*-

import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineProfile
from PyQt5.QtWidgets import QDialog

from ui_login_dlg import Ui_LoginDlg
from weibo import Weibo

logger = logging.getLogger(__name__)


class LoginDlg(QDialog, Ui_LoginDlg):

    def __init__(self):
        super().__init__(None, Qt.WindowMinimizeButtonHint
                         | Qt.WindowCloseButtonHint)
        self.setupUi(self)

        # 微博的登录凭证cookie
        self._weibo_cookies = {}

    def setupUi(self, login_dlg):
        super().setupUi(login_dlg)
        profile = self.web_view.page().profile()
        profile.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)
        profile.cookieStore().cookieAdded.connect(self._on_cookie_added)

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
