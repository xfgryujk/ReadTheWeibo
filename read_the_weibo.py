# -*- coding: utf-8 -*-

import pickle
import re
from logging import getLogger
from time import sleep

import pyttsx3

from login_dlg import LoginDlg
from weibo import Weibo

logger = getLogger(__name__)

DATA_DIR = 'data'
WEIBO_PATH = DATA_DIR + '/weibo.pickle'

TAG_REG = re.compile('<.*?>')


class ReadTheWeibo:

    def __init__(self):
        self.tts = pyttsx3.init()
        self.weibo = None

        self.load_weibo()
        # 登录
        if not self.weibo.is_login():
            dlg = LoginDlg()
            if not dlg.exec():
                return
            self.weibo.cookies = dlg.weibo_cookies

    def load_weibo(self):
        self.weibo = None
        try:
            with open(WEIBO_PATH, 'rb') as f:
                self.weibo = pickle.load(f)
        except OSError:  # 打开文件错误
            pass
        except pickle.PickleError:
            logger.exception('反序列化Weibo时出错：')
        if self.weibo is None:
            self.weibo = Weibo()

    def save_weibo(self):
        try:
            with open(WEIBO_PATH, 'wb') as f:
                self.weibo = pickle.dump(self.weibo, f)
        except OSError:  # 打开文件错误
            pass
        except pickle.PickleError:
            logger.exception('序列化Weibo时出错：')

    def run(self):
        while True:
            try:
                n_unread = self.weibo.get_n_unread()
                if n_unread > 0:
                    posts = self.weibo.get_friend_feed()[n_unread - 1::-1]

                    for post in posts:
                        user = post['user']['screen_name']
                        content = post['text']

                        logger.debug('%s：%s\n', user, content)

                        content = TAG_REG.sub('，', content)
                        self.tts.say('{}说：{}'.format(user, content))
                        self.tts.runAndWait()

            except:
                logger.exception('获取新微博时出错：')

            sleep(25)
