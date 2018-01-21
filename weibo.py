# -*- coding: utf-8 -*-

from requests import Session
from requests.cookies import cookiejar_from_dict


class Weibo:

    def __init__(self, cookies=None):
        self.session = Session()
        if cookies is not None:
            self.session.cookies = cookiejar_from_dict(cookies)

    def get_n_unread(self):
        res = self.session.get('https://m.weibo.cn/api/remind/unread')
        if not res.headers['X-Log-Uid']:
            print('Cookie过期！')
        return (res
                .json()['data']['unreadmblog'])

    def get_friend_feed(self, max_id=None):
        # 每页20个
        return (self.session.get('https://m.weibo.cn/feed/friends',
                                 params={'max_id': max_id or ''})
                .json()['data']['statuses'])
