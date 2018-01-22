# -*- coding: utf-8 -*-

from logging import getLogger

from requests import Session
from requests.cookies import RequestsCookieJar, cookiejar_from_dict

logger = getLogger(__name__)


class Weibo:

    def __init__(self, cookies=None):
        self.session = Session()
        if cookies is not None:
            self.cookies = cookies

    @property
    def cookies(self):
        return self.session.cookies

    @cookies.setter
    def cookies(self, value):
        if not isinstance(value, RequestsCookieJar):
            value = cookiejar_from_dict(value)
        self.session.cookies = value

    def _get(self, *args, **kwargs):
        """
        等价于self.session.get
        """

        res = self.session.get(*args, **kwargs)
        if not res.headers['X-Log-Uid']:
            logger.warning('Cookie过期！')
        return res

    def is_login(self):
        """
        :return: 是否已登录
        """

        return (self.session.get('https://m.weibo.cn/api/config')
                .json()['data']['login'])

    def get_n_unread(self):
        """
        :return: 未读微博数
        """

        return (self._get('https://m.weibo.cn/api/remind/unread')
                .json()['data']['unreadmblog'])

    def get_friend_feed(self, max_id=''):
        """
        取首页（关注）feed
        :param max_id: 最大微博ID，用来分页
        :return: 微博list，每页20个
        """

        return (self._get('https://m.weibo.cn/feed/friends',
                          params={'max_id': max_id})
                .json()['data']['statuses'])
