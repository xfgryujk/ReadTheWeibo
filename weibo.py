# -*- coding: utf-8 -*-

import re
from datetime import datetime
from logging import getLogger

from requests import Session
from requests.cookies import RequestsCookieJar, cookiejar_from_dict

logger = getLogger(__name__)

TAG_REG = re.compile('<.*?>')


class Post:
    """
    一条微博
    """

    def __init__(self, post=None):
        if post is None:
            self.user_name = ''
            self.avatar_url = ''
            self.create_time = datetime.now()
            # HTML内容
            self.raw_content = ''
            # 无HTML内容
            self.content = ''
            # 原微博，不是转发则为None
            self.original_post = None
        else:
            self.user_name = post['user']['screen_name']
            self.avatar_url = post['user']['profile_image_url']
            self.create_time = datetime.strptime(post['created_at'],
                                                 '%a %b %d %H:%M:%S %z %Y')
            self.raw_content = post['text']
            self.content = (post['raw_text'] if 'raw_text' in post
                            else TAG_REG.sub('', self.raw_content))
            self.original_post = (Post(post['retweeted_status']) if 'retweeted_status' in post
                                  else None)

    @property
    def is_repost(self):
        """
        是否是转发
        """

        return self.original_post is not None


class Weibo:
    """
    微博session、API
    """

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
        :return: Post列表，每页20个
        """

        posts = (self._get('https://m.weibo.cn/feed/friends',
                           params={'max_id': max_id})
                 .json()['data']['statuses'])
        return [Post(post) for post in posts]
